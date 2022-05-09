from typing import List


class UserHistory:
    def __init__(self, steps: List[str] = None):
        self.steps: List[str] = steps

    def __str__(self):
        return f"{self.steps}"
