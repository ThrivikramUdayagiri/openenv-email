import os
from openai import OpenAI
from env.environment import SmartEmailTriageEnv, ActionEasy, ActionMedium, ActionHard

API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
HF_TOKEN = os.getenv("HF_TOKEN")

def run_task(task_name, action_cls):
    env = SmartEmailTriageEnv(task_level=task_name)
    obs = env.reset()
    total_reward = 0.0
    print(f"START task={task_name}")
    for idx, expected in enumerate(env.task["expected"]):
        # Simulate a model prediction (replace with OpenAI call in real use)
        if task_name == "easy":
            # Simple rule-based for demo
            if "free" in obs.email_text or "offer" in obs.email_text or "buy" in obs.email_text:
                action = action_cls(label="spam")
            else:
                action = action_cls(label="not_spam")
        elif task_name == "medium":
            if "meeting" in obs.email_text or "review" in obs.email_text:
                action = action_cls(label="work")
            elif "order" in obs.email_text or "off" in obs.email_text:
                action = action_cls(label="promotions")
            else:
                action = action_cls(label="personal")
        else:
            if "urgent" in obs.email_text or "contract" in obs.email_text:
                action = action_cls(priority="high", action="reply")
            elif "flag" in obs.email_text:
                action = action_cls(priority="low", action="flag")
            elif "ignore" in obs.email_text:
                action = action_cls(priority="low", action="ignore")
            else:
                action = action_cls(priority="high", action="reply")
        print(f"STEP action={action.dict()}")
        obs, reward, done, info = env.step(action.dict())
        print(f"STEP reward={reward.value}")
        total_reward += reward.value
        if done:
            break
    # Bonus for perfect sequence
    if total_reward == len(env.task["expected"]):
        total_reward += 0.5
    print(f"END score={total_reward}")

if __name__ == "__main__":
    run_task("easy", ActionEasy)
    run_task("medium", ActionMedium)
    run_task("hard", ActionHard)
