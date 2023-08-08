from enum import Enum


class Environments(str, Enum):
    dev = "dev"
    stage = "stage"
    prd = "prd"
