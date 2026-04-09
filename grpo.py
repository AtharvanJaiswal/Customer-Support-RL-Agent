import asyncio
import json
import os
from client import CustomerSupportClient
from inference import llm_agent
from models import SupportAction


def generate_candidates(query, k=5):
    return [llm_agent(query) for _ in range(k)]


def to_action(data):
    return SupportAction(
        category=data["category"],
        priority=data["priority"],
        response=data["response"]
    )
def is_valid_response(text):
    if not text or len(text.strip()) < 15:
        return False

    bad_patterns = [
        "http",
        "www",
        "donate",
        "support me",
        "please help please help",
        "asdf",
    ]

    text_lower = text.lower()

    if any(p in text_lower for p in bad_patterns):
        return False

    return True

async def run_grpo():
    env = CustomerSupportClient(base_url="https://athiJais-customer-support-rl-agent.hf.space")

    dataset = []

    result = await env.reset()

    while not result.done:
        query = result.observation.customer_query

        print("\nQuery:", query)

        candidates = generate_candidates(query, k=5)

        scored = []

        for i, c in enumerate(candidates):
            action = to_action(c)

            temp_result = await env.step(action)

            reward = temp_result.reward or 0

            print(f"\nCandidate {i+1}")
            print("Action:", c)
            print("Reward:", reward)

            scored.append((c, reward))

        valid_candidates = [c for c in scored if is_valid_response(c[0]["response"])]

        if valid_candidates:
            best = max(valid_candidates, key=lambda x: x[1])
        else:
            best = max(scored, key=lambda x: x[1])

        print("\n🏆 BEST ACTION:", best[0], "Reward:", best[1])

        # ✅ SAVE BEST SAMPLE
        dataset.append({
            "query": query,
            "category": best[0]["category"],
            "priority": best[0]["priority"],
            "response": best[0]["response"],
            "reward": best[1]
        })

        # take best action in env
        result = await env.step(to_action(best[0]))

    # ✅ AFTER LOOP → merge dataset
    if os.path.exists("grpo_dataset.json"):
        with open("grpo_dataset.json", "r") as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    existing_data.extend(dataset)

    with open("grpo_dataset.json", "w") as f:
        json.dump(existing_data, f, indent=2)

    print(f"\n✅ Dataset updated! Total samples: {len(existing_data)}")


if __name__ == "__main__":
    asyncio.run(run_grpo())