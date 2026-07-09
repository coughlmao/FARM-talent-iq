from enum import StrEnum


class Difficulty(StrEnum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class SessionStatus(StrEnum):
    ACTIVE = "active"
    COMPLETED = "completed"
