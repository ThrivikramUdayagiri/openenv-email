
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal

app = FastAPI()

# Action classes for OpenEnv compatibility
class ActionEasy(BaseModel):
    spam: bool

class ActionMedium(BaseModel):
    category: Literal["work", "promotions", "personal"]

class ActionHard(BaseModel):
    priority: Literal["high", "low"]
    action: Literal["reply", "flag", "ignore"]

class EmailInput(BaseModel):
    subject: str
    body: str
    sender: str
    priority: str = "low"
    category: str = "personal"
    spam: bool = False
    action: str = "ignore"

@app.post("/reset")
def reset():
    return {"status": "ok"}

def log_task(task: str, action, reward: int, score: int):
    print(f"START task={task}")
    print(f"STEP action={action}")
    print(f"STEP reward={reward}")
    print(f"END score={score}")

def classify_easy(email: EmailInput):
    spam_keywords = ["win", "free", "prize", "money", "offer"]
    is_spam = any(word in email.subject.lower() or word in email.body.lower() for word in spam_keywords)
    action = ActionEasy(spam=is_spam)
    reward = int(is_spam == email.spam)
    score = reward
    log_task("easy", action.model_dump(), reward, score)
    return action.model_dump()

def classify_medium(email: EmailInput):
    work_keywords = ["meeting", "project", "deadline", "client"]
    promo_keywords = ["sale", "discount", "offer", "deal"]
    category = "personal"
    if any(word in email.subject.lower() or word in email.body.lower() for word in work_keywords):
        category = "work"
    elif any(word in email.subject.lower() or word in email.body.lower() for word in promo_keywords):
        category = "promotions"
    action = ActionMedium(category=category)
    reward = int(category == email.category)
    score = reward
    log_task("medium", action.model_dump(), reward, score)
    return action.model_dump()

def classify_hard(email: EmailInput):
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
    reward = int(priority == email.priority and action_type == email.action)
    score = reward
    log_task("hard", action.model_dump(), reward, score)
    return action.model_dump()

@app.post("/run_task/{task}")
def run_task(task: str, email: EmailInput):
    if task == "easy":
        return classify_easy(email)
    elif task == "medium":
        return classify_medium(email)
    elif task == "hard":
        return classify_hard(email)
    else:
        return {"error": "Unknown task"}