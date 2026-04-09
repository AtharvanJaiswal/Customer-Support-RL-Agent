"""
Task definitions with deterministic graders.
Each grader returns a score strictly between 0 and 1 (0.001 – 0.999).
"""

def grading_logic(task, action):
    score = 0.0

    category = action.get("category", "")
    priority = action.get("priority", "")
    response = (action.get("response") or "").lower()

    VALID_CATEGORIES = ["billing", "technical", "general"]
    VALID_PRIORITIES = ["low", "medium", "high"]

    # Category scoring
    if category == task["expected_category"]:
        score += 0.4
    elif category in VALID_CATEGORIES:
        score += 0.15

    # Priority scoring
    if priority == task["expected_priority"]:
        score += 0.25
    elif priority in VALID_PRIORITIES:
        score += 0.05

    # Response keyword scoring
    if any(kw in response for kw in task["keywords"]):
        score += 0.2

    # Tone scoring
    if any(w in response for w in ["sorry", "thank", "please", "assist", "help"]):
        score += 0.1

    # Response length penalty
    if len(response.strip()) < 10:
        score -= 0.15

    # Clamp strictly between (0, 1)
    score = max(0.001, min(score, 0.999))
    return round(score, 4)


# Individual graders (IMPORTANT)
def billing_grader(obs, action):
    return grading_logic(TASKS["billing_support"], action)

def technical_grader(obs, action):
    return grading_logic(TASKS["technical_support"], action)

def general_grader(obs, action):
    return grading_logic(TASKS["general_support"], action)


# Tasks WITH graders attached
TASKS = [
    {
        "id": "billing_support",
        "name": "Billing Support",
        "description": "Handle billing queries",
        "grader": billing_grader,
    },
    {
        "id": "technical_support",
        "name": "Technical Support",
        "description": "Handle technical issues",
        "grader": technical_grader,
    },
    {
        "id": "general_support",
        "name": "General Support",
        "description": "Handle general queries",
        "grader": general_grader,
    },
]