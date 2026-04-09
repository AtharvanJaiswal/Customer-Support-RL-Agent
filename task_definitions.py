"""
Task definitions with deterministic graders.
Each grader returns a score strictly between 0 and 1 (0.001 – 0.999).
"""

TASKS = {
    "billing_support": {
        "id": "billing_support",
        "name": "Billing Support",
        "description": "Handle billing queries: refunds, double charges, payment failures.",
        "difficulty": "medium",
        "sample_query": "I was charged twice for my order",
        "expected_category": "billing",
        "expected_priority": "high",
        "keywords": ["refund", "charged", "payment", "subscription"],
    },
    "technical_support": {
        "id": "technical_support",
        "name": "Technical Support",
        "description": "Handle technical issues: crashes, login failures, UI bugs.",
        "difficulty": "medium",
        "sample_query": "App crashes every time I open it",
        "expected_category": "technical",
        "expected_priority": "high",
        "keywords": ["crash", "error", "login", "freeze", "bug"],
    },
    "general_support": {
        "id": "general_support",
        "name": "General Support",
        "description": "Handle general queries: account management, password reset, how-to.",
        "difficulty": "easy",
        "sample_query": "How do I reset my password?",
        "expected_category": "general",
        "expected_priority": "low",
        "keywords": ["password", "account", "delete", "how", "help"],
    },
}


def grade(task_id: str, action: dict) -> float:
    """
    Grade an action against a task.
    Returns a score strictly between 0 and 1 (0.001 – 0.999).
    """
    task = TASKS.get(task_id)
    if task is None:
        return 0.1

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

    # Clamp strictly between 0 and 1
    score = max(0.001, min(score, 0.999))

    return round(score, 4)