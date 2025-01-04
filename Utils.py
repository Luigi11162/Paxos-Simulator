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
    COLLECT = 0
    BEGIN = 1
    SUCCESS = 2


def create_message(message_type, id_sender, values=None):
    return {"type": message_type, "sender": id_sender, "values": values}


def send(message):
    results = {}
    sender = message["sender"]
    for i in range(nodes):
        #Evito un auto_invio
        if i != sender:
            results[i] = voters[i].vote(message)

    return results

def choose_proposer(n):
    return randint(0, n - 1)

def compare_rounds(round1, round2):
    if round1[0] > round2[0]:
        return 1
    if round1[0] == round2[0] and round1[1] > round2[1]:
        return 0
    return -1