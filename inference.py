import os
from openai import OpenAI
from env.environment import SmartEmailTriageEnv, ActionEasy, ActionMedium, ActionHard

# Load environment variables
API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
HF_TOKEN = os.getenv("HF_TOKEN")

# Validate env variables
if not API_BASE_URL or not MODEL_NAME or not HF_TOKEN:
    raise ValueError("Missing required environment variables (API_BASE_URL, MODEL_NAME, HF_TOKEN)")

# Initialize OpenAI client
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

# ----------- PARSERS -----------

def parse_easy_output(text):
    text = text.lower()
    if "spam" in text:
        return {"label": "spam"}
    return {"label": "not_spam"}

def parse_medium_output(text):
    text = text.lower()
    if "work" in text:
        return {"label": "work"}
    elif "promotions" in text or "promotion" in text:
        return {"label": "promotions"}
    else:
        return {"label": "personal"}

def parse_hard_output(text):
    text = text.lower()
    priority = "high" if "high" in text else "low"

    if "reply" in text:
        action = "reply"
    elif "flag" in text:
        action = "flag"
    else:
        action = "ignore"

    return {"priority": priority, "action": action}

# ----------- MAIN TASK RUNNER -----------

def run_task(task_name, action_cls):
    env = SmartEmailTriageEnv(task_level=task_name)
    obs = env.reset()
    total_reward = 0.0

    print(f"START task={task_name}")

    for _ in env.task["expected"]:

        # Call OpenAI model
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are an email classification assistant."},
                {"role": "user", "content": obs.email_text}
            ]
        )

        model_output = response.choices[0].message.content

        # Parse model output into structured action
        if task_name == "easy":
            parsed = parse_easy_output(model_output)
            action = action_cls(**parsed)

        elif task_name == "medium":
            parsed = parse_medium_output(model_output)
            action = action_cls(**parsed)

        else:
            parsed = parse_hard_output(model_output)
            action = action_cls(**parsed)

        print(f"STEP action={action.dict()}")

        obs, reward, done, info = env.step(action.dict())

        print(f"STEP reward={reward.value}")

        total_reward += reward.value

        if done:
            break

    # Normalize score (0 → 1)
    max_score = len(env.task["expected"])
    final_score = total_reward / max_score if max_score > 0 else 0.0

    print(f"END score={final_score}")


# ----------- RUN ALL TASKS -----------

if __name__ == "__main__":
    run_task("easy", ActionEasy)
    run_task("medium", ActionMedium)
    run_task("hard", ActionHard)