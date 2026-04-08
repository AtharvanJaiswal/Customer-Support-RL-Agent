import uuid
import random
from openenv.core.env import Env
from models import SupportAction, SupportObservation, SupportState


# ✅ DATASET (expanded)
TICKETS = [
    # Billing
    {"query": "I was charged twice for my order", "category": "billing", "priority": "high", "keywords": ["refund", "charged", "double"]},
    {"query": "I want a refund for my subscription", "category": "billing", "priority": "high", "keywords": ["refund", "subscription"]},
    {"query": "Payment failed but money deducted", "category": "billing", "priority": "high", "keywords": ["payment", "failed"]},
    {"query": "Subscription cancelled but still charged", "category": "billing", "priority": "high", "keywords": ["charged"]},
    {"query": "Refund me NOW or I will complain", "category": "billing", "priority": "high", "keywords": ["refund", "urgent"]},

    # Technical
    {"query": "App crashes every time I open it", "category": "technical", "priority": "high", "keywords": ["crash", "error", "bug"]},
    {"query": "Login is not working on my phone", "category": "technical", "priority": "medium", "keywords": ["login", "error"]},
    {"query": "App freezes after login", "category": "technical", "priority": "high", "keywords": ["freeze", "login"]},
    {"query": "UI looks broken on my screen", "category": "technical", "priority": "medium", "keywords": ["ui", "bug"]},

    # General
    {"query": "How do I update my profile?", "category": "general", "priority": "low", "keywords": ["how", "help"]},
    {"query": "Where can I change my password?", "category": "general", "priority": "low", "keywords": ["password", "change"]},
    {"query": "Cannot reset my password", "category": "general", "priority": "medium", "keywords": ["password"]},
    {"query": "How do I delete my account?", "category": "general", "priority": "low", "keywords": ["delete"]},

    # Edge cases 🔥
    {"query": "Why was I charged AND the app crashed?", "category": "technical", "priority": "high", "keywords": ["crash", "charged"]},
    {"query": "This service is terrible!!!", "category": "general", "priority": "medium", "keywords": ["bad", "complaint"]},
    {"query": "Thanks, my issue is already solved", "category": "general", "priority": "low", "keywords": ["thanks"]},
]


class CustomerSupportEnv(Environment):

    def __init__(self):
        self._state = SupportState()
        self._tickets = []
        self._index = 0
        self._current = None
        self.history = []

    # ✅ Query variation (IMPORTANT)
    def augment_query(self, q):
        variations = [
            q,
            q.lower(),
            q + " please help",
            "URGENT: " + q,
            q + " asap",
        ]
        return random.choice(variations)

    def reset(self, **kwargs):
        # ✅ Random sampling with duplicates (more variation)
        self._tickets = random.choices(TICKETS, k=20)
        self._index = 0
        self.history = []

        self._state = SupportState(
            episode_id=str(uuid.uuid4()),
            step_count=0,
            total_tickets=len(self._tickets),
            tickets_processed=0
        )

        self._current = self._tickets[self._index]

        # ✅ Apply variation
        self._current["query"] = self.augment_query(self._current["query"])

        return SupportObservation(
            ticket_id=str(self._index),
            customer_query=self._current["query"],
            done=False
        )

    def step(self, action: SupportAction):

        if self._current is None:
            return SupportObservation(
                ticket_id="end",
                customer_query="",
                reward=0.0,
                done=True
            )

        self._state.step_count += 1
        expected = self._current

        reward = 0.0

        VALID_CATEGORIES = ["billing", "technical", "general"]
        VALID_PRIORITIES = ["low", "medium", "high"]

        # ❌ invalid inputs
        if action.priority not in VALID_PRIORITIES:
            reward -= 0.2
        if action.category not in VALID_CATEGORIES:
            reward -= 0.3
        elif action.category != expected["category"]:
            reward -= 0.1

        # ✅ Category scoring
        if action.category == expected["category"]:
            reward += 0.4
        elif action.category in VALID_CATEGORIES:
            reward += 0.2

        # ✅ Priority scoring
        if action.priority == expected["priority"]:
            reward += 0.2

        # ✅ Response relevance
        response = (action.response or "").lower()

        if any(k in response for k in expected["keywords"]):
            reward += 0.2

        # ✅ Tone
        if any(word in response for word in ["sorry", "thank", "please"]):
            reward += 0.1

        # ✅ Special case
        if "already solved" in expected["query"].lower():
            if "glad" in response or "resolved" in response:
                reward += 0.3

        # ❌ too short
        if len(response.strip()) < 10:
            reward -= 0.2

        # ✅ memory
        self.history.append({
            "query": expected["query"],
            "action": action.category,
            "reward": reward
        })

        # ✅ update state
        self._state.tickets_processed += 1

        # 👉 next ticket
        self._index += 1
        done = self._index >= len(self._tickets)

        if done:
            reward += 0.1
            self._current = None
            query = ""
        else:
            self._current = self._tickets[self._index]
            self._current["query"] = self.augment_query(self._current["query"])
            query = self._current["query"]

        reward = max(0.0, min(reward, 1.0))

        return SupportObservation(
            ticket_id=str(self._index),
            customer_query=query,
            reward=reward,
            done=done
        )

    @property
    def state(self):
        return {
            "tickets_processed": self._state.tickets_processed,
            "total_tickets": self._state.total_tickets,
            "history": self.history[-3:]
        }
