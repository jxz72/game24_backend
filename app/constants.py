import operator
from enum import Enum

VALID_NUMBERS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']

VALID_OPERATIONS = {"add": operator.add, "sub": operator.sub, "mul": operator.mul, "div": operator.truediv}

class GameStatuses(Enum):
    COMPLETED = "completed"
    IN_PROGRESS = "in_progress"

