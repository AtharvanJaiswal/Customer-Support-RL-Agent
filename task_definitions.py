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

    return min(max(score, 0.01), 0.99)


# ✅ REQUIRED: function returning tasks
def get_tasks():
    return [
        {
            "id": "billing_support",
            "description": "Billing issues",
            "expected_category": "billing",
            "expected_priority": "high",
            "keywords": ["refund", "charged"],
            "grader": lambda obs, action: grading_logic({
                "expected_category": "billing",
                "expected_priority": "high",
                "keywords": ["refund", "charged"]
            }, action)
        },
        {
            "id": "technical_support",
            "description": "Technical issues",
            "expected_category": "technical",
            "expected_priority": "high",
            "keywords": ["crash", "error"],
            "grader": lambda obs, action: grading_logic({
                "expected_category": "technical",
                "expected_priority": "high",
                "keywords": ["crash", "error"]
            }, action)
        },
        {
            "id": "general_support",
            "description": "General queries",
            "expected_category": "general",
            "expected_priority": "low",
            "keywords": ["help", "account"],
            "grader": lambda obs, action: grading_logic({
                "expected_category": "general",
                "expected_priority": "low",
                "keywords": ["help", "account"]
            }, action)
        }
    ]