import os
from env.environment import SmartEmailTriageEnv, ActionEasy, ActionMedium, ActionHard

API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "openai/gpt-oss-120b")
HF_TOKEN = os.getenv("HF_TOKEN")

# ----------- RULE LOGIC -----------

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
    if any(x in text for x in ["urgent", "asap", "important"]):
        return {"priority": "high", "action": "reply"}
    elif any(x in text for x in ["reminder", "later"]):
        return {"priority": "low", "action": "flag"}
    return {"priority": "low", "action": "ignore"}


# ----------- CORE LOGIC -----------

def run_task(task_name, action_cls):
    env = SmartEmailTriageEnv(task_level=task_name)
    obs = env.reset()
    total_reward = 0.0

    print(f"START task={task_name}")

    for _ in env.task["expected"]:

        if task_name == "easy":
            parsed = classify_easy(obs.email_text)
        elif task_name == "medium":
            parsed = classify_medium(obs.email_text)
        else:
            parsed = classify_hard(obs.email_text)

        action = action_cls(**parsed)

        print(f"STEP action={action.model_dump()}")

        obs, reward, done, _ = env.step(action.model_dump())

        print(f"STEP reward={reward.value}")

        total_reward += reward.value

        if done:
            break

    final_score = total_reward / len(env.task["expected"])
    print(f"END score={final_score}")

    return {"score": final_score}



# ----------- MAIN ENTRY POINT -----------

if __name__ == "__main__":
    run_task("easy", ActionEasy)
    run_task("medium", ActionMedium)
    run_task("hard", ActionHard)