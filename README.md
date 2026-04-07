# openenv-email

**Smart Email Triage Environment (OpenEnv-compliant)**

## Overview
This project simulates a real-world email triage environment for reinforcement learning and LLM evaluation. It is fully OpenEnv-compliant and supports three task difficulties.

## Features
- **Observation:** Email text (string)
- **Action:**
  - Easy: `label` ('spam' or 'not_spam')
  - Medium: `label` ('work', 'personal', 'promotions')
  - Hard: `priority` ('high'/'low'), `action` ('reply'/'ignore'/'flag')
- **Reward:** +1 for correct, -0.5 for incorrect, bonus for perfect sequence
- **Grader:** Deterministic, task-specific scoring

## Project Structure
```
openenv-email/
├── env/
│   ├── environment.py
│   ├── tasks.py
│   └── grader.py
├── inference.py
├── requirements.txt
├── openenv.yaml
├── Dockerfile
└── README.md
```

## Tasks
- **Easy:** Classify as 'spam' or 'not_spam'
- **Medium:** Classify as 'work', 'personal', or 'promotions'
- **Hard:** Assign 'priority' and 'action'

## Setup
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **(Optional) Set environment variables:**
   - `API_BASE_URL`
   - `MODEL_NAME`
   - `HF_TOKEN`

## Running
```bash
python inference.py
```

## Docker
Build and run with Docker:
```bash
docker build -t openenv-email .
docker run --rm openenv-email
```

## OpenEnv Validation
This environment implements the OpenEnv interface and passes validation.

## License
MIT
