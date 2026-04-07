---
title: OpenEnv Email Triage
emoji: "\ud83d\udce7"
colorFrom: blue
colorTo: green
sdk: docker
app_file: inference.py
pinned: false
---

# OpenEnv Email Triage

A Hugging Face Space for OpenEnv email triage using FastAPI and rule-based logic.

## Features
- `/reset` endpoint for OpenEnv validation
- `/run_task/{task}` endpoint for easy, medium, and hard tasks
- Structured logging for OpenEnv evaluation
- Dockerized for Hugging Face Spaces

## Usage
1. Build the Docker image:
   ```sh
   docker build -t openenv-email .
   ```
2. Run the container:
   ```sh
   docker run -p 7860:7860 openenv-email
   ```
3. Access the API at `http://localhost:7860/reset` and `/run_task/{task}`

## Requirements
- Python 3.10+
- See requirements.txt
