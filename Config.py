from enum import Enum

values = [1, 2, 3, 4, 5]
proposers = []
voters = []
HOST = "127.0.0.1"
PORT = 5000

class MessageTypeVoter(Enum):
    OLD_ROUND = 0
    LAST_ROUND = 1
    ACCEPT = 2
    ACK = 3


class MessageTypeProposer(Enum):
    COLLECT = 0
    BEGIN = 1
    SUCCESS = 2