from enum import Enum

## Enum for the different states of the game
class State(Enum):
    START = 1
    REVEAL = 2
    SANCTUARY = 3
    REGION = 4
    COMPUTE = 5
    END = 6
    