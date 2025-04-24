import operator
from enum import Enum

VALID_OPERATIONS = {"add": operator.add, "sub": operator.sub, "mul": operator.mul, "div": operator.truediv}

class GameStatuses(Enum):
    COMPLETED = "completed"
    IN_PROGRESS = "in_progress"