from random import randint
from enum import Enum

global nodes
global proposers
global voters

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
    return {"type": message_type, "sender": id_sender, **values}


async def send(message):
    sender = message["sender"]
    for i in range(nodes):
        #Evito un auto_invio
        if i == sender:
            continue

        match message["type"]:
            case MessageTypeVoter.ACCEPT:
                await proposers[i].receive_accept(message)
            case MessageTypeVoter.OLD_ROUND:
                await proposers[i].receive_old_round(message)
            case MessageTypeVoter.LAST_ROUND:
                await proposers[i].receive_last_round(message)
            case MessageTypeProposer.BEGIN:
                await voters[i].vote(message)
            case MessageTypeProposer.PROPOSE:
                await voters[i].vote(message)
            case MessageTypeProposer.SUCCESS:
                await voters[i].vote(message)
            case _:
                raise TypeError("Invalid message type")


def choose_proposer(n):
    return randint(0, n - 1)
