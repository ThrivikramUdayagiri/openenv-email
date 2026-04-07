# Grader logic for Smart Email Triage
from typing import Any, Dict

def grader_easy(action: Dict, expected: Dict) -> float:
    return 1.0 if action["label"] == expected["label"] else -0.5

def grader_medium(action: Dict, expected: Dict) -> float:
    return 1.0 if action["label"] == expected["label"] else -0.5

def grader_hard(action: Dict, expected: Dict) -> float:
    score = 0.0
    if action.get("priority") == expected.get("priority"):
        score += 0.5
    else:
        score -= 0.25
    if action.get("action") == expected.get("action"):
        score += 0.5
    else:
        score -= 0.25
    return score

def get_grader(level: str):
    if level == "easy":
        return grader_easy
    elif level == "medium":
        return grader_medium
    elif level == "hard":
        return grader_hard
    else:
        raise ValueError(f"Unknown grader level: {level}")
