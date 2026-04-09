import uuid
import random

from openenv.core.env_server import Environment

try:
    from models import SupportAction, SupportObservation, SupportState
except ImportError:
    from models import SupportAction, SupportObservation, SupportState

TICKETS = [
    # Billing
    {"query": "I was charged twice for my order", "category": "billing", "priority": "high", "keywords": ["refund", "charged", "double"], "task": "billing_support"},
    {"query": "I want a refund for my subscription", "category": "billing", "priority": "high", "keywords": ["refund", "subscription"], "task": "billing_support"},
    {"query": "Payment failed but money deducted", "category": "billing", "priority": "high", "keywords": ["payment", "failed"], "task": "billing_support"},
    {"query": "Subscription cancelled but still charged", "category": "billing", "priority": "high", "keywords": ["charged"], "task": "billing_support"},
    {"query": "Refund me NOW or I will complain", "category": "billing", "priority": "high", "keywords": ["refund", "urgent"], "task": "billing_support"},

    # Technical
    {"query": "App crashes every time I open it", "category": "technical", "priority": "high", "keywords": ["crash", "error", "bug"], "task": "technical_support"},
    {"query": "Login is not working on my phone", "category": "technical", "priority": "medium", "keywords": ["login", "error"], "task": "technical_support"},
    {"query": "App freezes after login", "category": "technical", "priority": "high", "keywords": ["freeze", "login"], "task": "technical_support"},
    {"query": "UI looks broken on my screen", "category": "technical", "priority": "medium", "keywords": ["ui", "bug"], "task": "technical_support"},

    # General
    {"query": "How do I update my profile?", "category": "general", "priority": "low", "keywords": ["how", "help"], "task": "general_support"},
    {"query": "Where can I change my password?", "category": "general", "priority": "low", "keywords": ["password", "change"], "task": "general_support"},
    {"query": "Cannot reset my password", "category": "general", "priority": "medium", "keywords": ["password"], "task": "general_support"},
    {"query": "How do I delete my account?", "category": "general", "priority": "low", "keywords": ["delete"], "task": "general_support"},

    # Edge cases
    {"query": "Why was I charged AND the app crashed?", "category": "technical", "priority": "high", "keywords": ["crash", "charged"], "task": "technical_support"},
    {"query": "This service is terrible!!!", "category": "general", "priority": "medium", "keywords": ["bad", "complaint"], "task": "general_support"},
    {"query": "Thanks, my issue is already solved", "category": "general", "priority": "low", "keywords": ["thanks"], "task": "general_support"},
]


class CustomerSupportEnv(Environment):

    def __init__(self):
        self._state = SupportState()
        self._tickets = []
        self._index = 0
        self._current = None
        self.history = []

    def augment_query(self, q):
        variations = [q, q.lower(), q + " please help", "URGENT: " + q, q + " asap"]
        return random.choice(variations)

    def reset(self, **kwargs):
        billing = [t for t in TICKETS if t["task"] == "billing_support"]
        technical = [t for t in TICKETS if t["task"] == "technical_support"]
        general = [t for t in TICKETS if t["task"] == "general_support"]

        guaranteed = [random.choice(billing), random.choice(technical), random.choice(general)]
        rest = random.choices(TICKETS, k=17)
        self._tickets = guaranteed + rest
        random.shuffle(self._tickets)

        self._index = 0
        self.history = []

        self._state = SupportState(
            episode_id=str(uuid.uuid4()),
            step_count=0,
            total_tickets=len(self._tickets),
            tickets_processed=0
        )

        self._current = dict(self._tickets[self._index])
        self._current["query"] = self.augment_query(self._current["query"])

        return SupportObservation(
            ticket_id=str(self._index),
            customer_query=self._current["query"],
            done=False
        )

    def step(self, action: SupportAction):
        if self._current is None:
            return SupportObservation(ticket_id="end", customer_query="", reward=0.5, done=True)

        self._state.step_count += 1
        expected = self._current
        reward = 0.0

        VALID_CATEGORIES = ["billing", "technical", "general"]
        VALID_PRIORITIES = ["low", "medium", "high"]

        if action.priority not in VALID_PRIORITIES:
            reward -= 0.15
        if action.category not in VALID_CATEGORIES:
            reward -= 0.2
        elif action.category != expected["category"]:
            reward -= 0.1

        if action.category == expected["category"]:
            reward += 0.4
        elif action.category in VALID_CATEGORIES:
            reward += 0.15

        if action.priority == expected["priority"]:
            reward += 0.2

        response = (action.response or "").lower()
        if any(k in response for k in expected["keywords"]):
            reward += 0.2
        if any(w in response for w in ["sorry", "thank", "please"]):
            reward += 0.1
        if "already solved" in expected["query"].lower():
            if "glad" in response or "resolved" in response:
                reward += 0.15
        if len(response.strip()) < 10:
            reward -= 0.15

        self.history.append({
            "query": expected["query"],
            "action": action.category,
            "reward": reward,
            "task": expected.get("task", "general_support")
        })

        self._state.tickets_processed += 1
        self._index += 1
        done = self._index >= len(self._tickets)

        if done:
            self._current = None
            query = ""
        else:
            self._current = dict(self._tickets[self._index])
            self._current["query"] = self.augment_query(self._current["query"])
            query = self._current["query"]

        # Strictly between 0 and 1
        reward = max(0.001, min(reward, 0.999))

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