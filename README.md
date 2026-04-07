# openenv-email

A Hugging Face Space using FastAPI for OpenEnv email triage tasks.

## Features
- `/reset` endpoint for OpenEnv validation
- Rule-based email classification endpoints for easy, medium, and hard tasks
- Structured logging for each classification
- Dockerized for easy deployment

## Usage
1. Build the Docker image:
   ```sh
   docker build -t openenv-email .
   ```
2. Run the container:
   ```sh
   docker run -p 7860:7860 openenv-email
   ```
3. Access the API at `http://localhost:7860/reset` (and other endpoints)

## Endpoints
- `POST /reset`: Health check for OpenEnv
- `POST /classify/easy`: Spam detection
- `POST /classify/medium`: Category detection
- `POST /classify/hard`: Priority and action detection

## Requirements
- Python 3.10+
- See requirements.txt
