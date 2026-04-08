import asyncio
import random
from collections import defaultdict
from client import CustomerSupportClient
from inference import llm_agent
from models import SupportAction

Q = defaultdict(lambda: defaultdict(float))

alpha = 0.1
gamma = 0.9
epsilon = 0.3


def get_state_key(result):
    return result.observation.customer_query


def random_action(query):
    return {
        "category": random.choice(["billing", "technical", "general"]),
        "priority": random.choice(["low", "medium", "high"]),
        "response": f"Auto-response for: {query}"
    }


def choose_action(query, state_key):
    if random.random() < epsilon:
        return SupportAction(
            category=random.choice(["billing", "technical", "general"]),
            priority=random.choice(["low", "medium", "high"]),
            response=f"Auto-response for: {query}"
        )

    if state_key in Q and Q[state_key]:
        import ast
        best = ast.literal_eval(max(Q[state_key], key=Q[state_key].get))
        return SupportAction(**best)

    data = llm_agent(query)

    return SupportAction(
        category=data["category"],
        priority=data["priority"],
        response=data["response"]
    )


def update_q(state_key, action, reward, next_state_key):
    action_key = str({
    "category": action.category,
    "priority": action.priority,
    "response": action.response
})
    best_next = max(Q[next_state_key].values(), default=0)

    Q[state_key][action_key] += alpha * (
        reward + gamma * best_next - Q[state_key][action_key]
    )


async def train(episodes=5):
    env = CustomerSupportClient(base_url="http://localhost:8000")

    for ep in range(episodes):
        print(f"\n🔥 EPISODE {ep+1}")

        result = await env.reset()

        total_reward = 0
        steps = 0

        while not result.done:
            query = result.observation.customer_query
            state_key = get_state_key(result)

            print("\nQuery:", query)

            action = choose_action(query, state_key)
            print("Action:", action.category, action.priority)
            

            result_next = await env.step(action)

            reward = result_next.reward or 0

            print("Reward:", reward)

            next_state_key = get_state_key(result_next)

            update_q(state_key, action, reward, next_state_key)

            total_reward += reward
            steps += 1

            result = result_next

        print("\n📊 RESULT")
        print("Steps:", steps)
        print("Total Reward:", total_reward)
        

if __name__ == "__main__":
    asyncio.run(train(episodes=10))