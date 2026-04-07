import os
from openai import OpenAI
from env.environment import SmartEmailTriageEnv, ActionEasy, ActionMedium, ActionHard

# ----------- ENV VARIABLES (REQUIRED BY CHECKLIST) -----------

API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "openai/gpt-oss-120b")
HF_TOKEN = os.getenv("HF_TOKEN")

# Initialize client safely
client = None
if HF_TOKEN:
    client = OpenAI(
        base_url=API_BASE_URL,
        api_key=HF_TOKEN
    )

# ----------- RULE-BASED LOGIC -----------

def classify_easy(text):
    text = text.lower()
    if any(x in text for x in ["free", "offer", "buy", "win", "prize"]):
        return {"label": "spam"}
    return {"label": "not_spam"}


def classify_medium(text):
    text = text.lower()
    if any(x in text for x in ["meeting", "review", "project", "deadline", "client"]):
        return {"label": "work"}
    elif any(x in text for x in ["offer", "sale", "discount", "deal"]):
        return {"label": "promotions"}
    else:
        return {"label": "personal"}


def classify_hard(text):
    text = text.lower()

    if any(x in text for x in ["urgent", "asap", "important", "immediately"]):
        return {"priority": "high", "action": "reply"}

    elif any(x in text for x in ["reminder", "later", "follow up"]):
        return {"priority": "low", "action": "flag"}

    else:
        return {"priority": "low", "action": "ignore"}


# ----------- MAIN TASK RUNNER -----------

def run_task(task_name, action_cls):
    env = SmartEmailTriageEnv(task_level=task_name)
    obs = env.reset()
    total_reward = 0.0

    print(f"START task={task_name}")

    for _ in env.task["expected"]:

        if task_name == "easy":
            parsed = classify_easy(obs.email_text)
            action = action_cls(**parsed)

        elif task_name == "medium":
            parsed = classify_medium(obs.email_text)
            action = action_cls(**parsed)

        else:
            parsed = classify_hard(obs.email_text)
            action = action_cls(**parsed)

        print(f"STEP action={action.model_dump()}")

        obs, reward, done, info = env.step(action.model_dump())

        print(f"STEP reward={reward.value}")

        total_reward += reward.value

        if done:
            break

    max_score = len(env.task["expected"])
    final_score = total_reward / max_score if max_score > 0 else 0.0

    print(f"END score={final_score}")


# ----------- RUN ALL TASKS -----------

if __name__ == "__main__":
    run_task("easy", ActionEasy)
    run_task("medium", ActionMedium)
    run_task("hard", ActionHard)