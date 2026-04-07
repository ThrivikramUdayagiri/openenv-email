from typing import Any, Dict, Tuple
from pydantic import BaseModel
from .tasks import TASKS, get_task
from .grader import get_grader
import random

class Observation(BaseModel):
    email_text: str

class ActionEasy(BaseModel):
    label: str  # 'spam' or 'not_spam'

class ActionMedium(BaseModel):
    label: str  # 'work', 'personal', 'promotions'

class ActionHard(BaseModel):
    priority: str  # 'high' or 'low'
    action: str    # 'reply', 'ignore', 'flag'

class Reward(BaseModel):
    value: float

class SmartEmailTriageEnv:
    def __init__(self, task_level: str = "easy"):
        self.task_level = task_level
        self.task = get_task(task_level)
        self.grader = get_grader(task_level)
        self.idx = 0
        self.done = False
        self.episode = []
        self._reset_state()

    def _reset_state(self):
        self.idx = 0
        self.done = False
        self.episode = []
        self.emails = self.task["emails"]
        self.expected = self.task["expected"]

    def reset(self) -> Observation:
        self._reset_state()
        return Observation(email_text=self.emails[self.idx])

    def step(self, action: Any) -> Tuple[Observation, Reward, bool, Dict]:
        expected = self.expected[self.idx]
        reward = self.grader(action, expected)
        self.episode.append((action, expected, reward))
        self.idx += 1
        if self.idx >= len(self.emails):
            self.done = True
            obs = Observation(email_text="")
        else:
            obs = Observation(email_text=self.emails[self.idx])
        return obs, Reward(value=reward), self.done, {}

    def state(self):
        return {
            "idx": self.idx,
            "done": self.done,
            "episode": self.episode
        }
