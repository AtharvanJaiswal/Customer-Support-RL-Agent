def safe_score(x):
    return max(0.05, min(x, 0.95))


def billing_grader(obs, action):
    score = 0.5

    if action.get("category") == "billing":
        score += 0.3
    else:
        score -= 0.1

    if action.get("priority") == "high":
        score += 0.1

    if "refund" in (action.get("response") or "").lower():
        score += 0.1

    return safe_score(score)


def technical_grader(obs, action):
    score = 0.5

    if action.get("category") == "technical":
        score += 0.3
    else:
        score -= 0.1

    if action.get("priority") == "high":
        score += 0.1

    if "error" in (action.get("response") or "").lower():
        score += 0.1

    return safe_score(score)


def general_grader(obs, action):
    score = 0.5

    if action.get("category") == "general":
        score += 0.3
    else:
        score -= 0.1

    if action.get("priority") in ["low", "medium"]:
        score += 0.1

    if "help" in (action.get("response") or "").lower():
        score += 0.1

    return safe_score(score)


def get_tasks():
    return [
        {
            "id": "billing_support",
            "name": "Billing Support",
            "description": "Billing queries",
            "grader": billing_grader,
        },
        {
            "id": "technical_support",
            "name": "Technical Support",
            "description": "Technical issues",
            "grader": technical_grader,
        },
        {
            "id": "general_support",
            "name": "General Support",
            "description": "General queries",
            "grader": general_grader,
        },
    ]