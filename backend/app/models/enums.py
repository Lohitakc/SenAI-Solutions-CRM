from enum import Enum


class Status(str, Enum):
    OPEN = "OPEN"
    PENDING = "PENDING"
    CLOSED = "CLOSED"
    ESCALATED = "ESCALATED"


class Priority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
