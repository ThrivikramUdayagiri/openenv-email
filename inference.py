from fastapi import FastAPI, Request
from env.environment import SmartEmailTriageEnv, ActionEasy, ActionMedium, ActionHard
from pydantic import BaseModel
from typing import Any, Dict

app = FastAPI()

def log_easy(action, reward, score):
    print("START task=easy")
    print(f"STEP action={action}")
    print(f"STEP reward={reward}")
    print(f"END score={score}")

def log_medium(action, reward, score):
    print("START task=medium")
    print(f"STEP action={action}")
    print(f"STEP reward={reward}")
    print(f"END score={score}")

def log_hard(action, reward, score):
    print("START task=hard")
    print(f"STEP action={action}")
    print(f"STEP reward={reward}")
    print(f"END score={score}")

class EmailInput(BaseModel):
    subject: str
    body: str
    sender: str
    priority: str = "low"
    category: str = "personal"
    spam: bool = False

@app.post("/reset")
def reset():
    return {"status": "ok"}

@app.post("/classify/easy")
def classify_easy(email: EmailInput):
    # Rule-based spam detection
    spam_keywords = ["win", "free", "prize", "money", "offer"]
    is_spam = any(word in email.subject.lower() or word in email.body.lower() for word in spam_keywords)
    action = ActionEasy(spam=is_spam)
    reward = 1 if is_spam == email.spam else 0
    score = reward
    log_easy(action.model_dump(), reward, score)
    return action.model_dump()

@app.post("/classify/medium")
def classify_medium(email: EmailInput):
    # Rule-based category detection
    work_keywords = ["meeting", "project", "deadline", "client"]
    promo_keywords = ["sale", "discount", "offer", "deal"]
    category = "personal"
    if any(word in email.subject.lower() or word in email.body.lower() for word in work_keywords):
        category = "work"
    elif any(word in email.subject.lower() or word in email.body.lower() for word in promo_keywords):
        category = "promotions"
    action = ActionMedium(category=category)
    reward = 1 if category == email.category else 0
    score = reward
    log_medium(action.model_dump(), reward, score)
    return action.model_dump()

@app.post("/classify/hard")
def classify_hard(email: EmailInput):
    # Rule-based priority and action
    high_priority_keywords = ["urgent", "asap", "important", "immediate"]
    reply_keywords = ["reply", "respond", "question"]
    flag_keywords = ["follow up", "reminder", "flag"]
    priority = "low"
    action_type = "ignore"
    if any(word in email.subject.lower() or word in email.body.lower() for word in high_priority_keywords):
        priority = "high"
    if any(word in email.subject.lower() or word in email.body.lower() for word in reply_keywords):
        action_type = "reply"
    elif any(word in email.subject.lower() or word in email.body.lower() for word in flag_keywords):
        action_type = "flag"
    action = ActionHard(priority=priority, action=action_type)
    reward = 1 if priority == email.priority and action_type == email.action else 0
    score = reward
    log_hard(action.model_dump(), reward, score)
    return action.model_dump()
