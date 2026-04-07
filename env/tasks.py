# Task definitions for Smart Email Triage
from typing import Dict, Any

def get_task(level: str) -> Dict[str, Any]:
    if level == "easy":
        return TASKS["easy"]
    elif level == "medium":
        return TASKS["medium"]
    elif level == "hard":
        return TASKS["hard"]
    else:
        raise ValueError(f"Unknown task level: {level}")

TASKS = {
    "easy": {
        "emails": [
            "Congratulations! You've won a free cruise. Click here to claim.",
            "Hi team, please find attached the project report.",
            "Limited time offer! Buy now and save 50%.",
            "Let's catch up for coffee this weekend."
        ],
        "expected": [
            {"label": "spam"},
            {"label": "not_spam"},
            {"label": "spam"},
            {"label": "not_spam"}
        ]
    },
    "medium": {
        "emails": [
            "Quarterly review meeting scheduled for Monday.",
            "Your Amazon order has shipped!",
            "Dinner at my place tomorrow night?",
            "50% off on your favorite brands!"
        ],
        "expected": [
            {"label": "work"},
            {"label": "promotions"},
            {"label": "personal"},
            {"label": "promotions"}
        ]
    },
    "hard": {
        "emails": [
            "Please review and reply to the attached contract by EOD.",
            "Don't forget to flag this for your records.",
            "Let's ignore this chain for now.",
            "URGENT: Server is down, immediate action required!"
        ],
        "expected": [
            {"priority": "high", "action": "reply"},
            {"priority": "low", "action": "flag"},
            {"priority": "low", "action": "ignore"},
            {"priority": "high", "action": "reply"}
        ]
    }
}
