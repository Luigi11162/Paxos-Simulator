from random import randint
from Main import proposers, i
from enum import Enum

class MessageTypeVoter(Enum):
    ACCEPT = 0
    OLD_ROUND = 1
    LAST_ROUND = 2
    ACK = 3

class MessageTypeProposer(Enum):
    BEGIN = 0
    PROPOSE = 1
    SUCCESS = 2

def create_message(message_type, id_sender, **values):
    return {"type": message_type,"id": id_sender, **values}

async def send(message):
    match message["type"]:
        case MessageTypeVoter.ACCEPT:
            await proposers[i].receive_accept(message)
        case MessageTypeVoter.OLD_ROUND:
            await proposers[i].receive_old_round(message)
        case MessageTypeVoter.LAST_ROUND:
            await proposers[i].receive_last_round(message)
        case MessageTypeProposer.BEGIN:
            await proposers[i].receive_begin(message)
        case MessageTypeProposer.PROPOSE:
            await proposers[i].receive_propose(message)
        case MessageTypeProposer.SUCCESS:
            await proposers[i].receive_success(message)
        case _:
            raise Exception("Invalid message type")


def choose_proposer(n):
    return randint(0,n-1)