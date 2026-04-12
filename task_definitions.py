"""
Task definitions with deterministic graders.
"""

def grading_logic(task, action):
    score = 0.0

    category = action.get("category", "")
    priority = action.get("priority", "")
    response = (action.get("response") or "").lower()

    if category == task["expected_category"]:
        score += 0.4
    else:
        score += 0.1

    if priority == task["expected_priority"]:
        score += 0.3
    else:
        score += 0.1

    if any(kw in response for kw in task["keywords"]):
        score += 0.2

    if len(response) > 10:
        score += 0.1

    # 🚨 CRITICAL: never allow 0 or 1
    score = max(0.05, min(score, 0.95))
    return score


# ✅ Named graders (IMPORTANT)
def billing_grader(obs, action):
    return grading_logic({
        "expected_category": "billing",
        "expected_priority": "high",
        "keywords": ["refund", "charged"]
    }, action)


def technical_grader(obs, action):
    return grading_logic({
        "expected_category": "technical",
        "expected_priority": "high",
        "keywords": ["crash", "error"]
    }, action)


def general_grader(obs, action):
    return grading_logic({
        "expected_category": "general",
        "expected_priority": "low",
        "keywords": ["help", "account"]
    }, action)


# ✅ REQUIRED FUNCTION
def get_tasks():
    return [
        {
            "id": "billing_support",
            "name": "Billing Support",  # ✅ ADD THIS
            "description": "Billing issues",
            "grader": billing_grader,
        },
        {
            "id": "technical_support",
            "name": "Technical Support",  # ✅ ADD THIS
            "description": "Technical issues",
            "grader": technical_grader,
        },
        {
            "id": "general_support",
            "name": "General Support",  # ✅ ADD THIS
            "description": "General queries",
            "grader": general_grader,
        }
    ]