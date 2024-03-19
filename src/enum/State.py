from enum import Enum

## Enum for the different states of the game
class State(Enum):
    START = 1
    PSEUDO = 2
    REVEAL = 3
    SANCTUARY = 4
    REGION = 5
    COMPUTE = 6
    END = 7
    