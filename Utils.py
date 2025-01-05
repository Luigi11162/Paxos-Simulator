from random import randint
from enum import Enum

nodes = 5
values = [1, 2, 3, 4, 5]
proposers = []
voters = []


class MessageTypeVoter(Enum):
    OLD_ROUND = 0
    LAST_ROUND = 1
    ACCEPT = 2
    ACK = 3


class MessageTypeProposer(Enum):
    COLLECT = 0
    BEGIN = 1
    SUCCESS = 2


def create_message(message_type, id_sender, message_values=None):
    return {"type": message_type, "sender": id_sender, "values": message_values}


def choose_proposer(n):
    return randint(0, n - 1)

def compare_rounds(round1, round2):
    if round1[0] > round2[0] or round1[0] == round2[0] and round1[1] > round2[1]:
        return 1
    if round1[0] == round2[0] and round1[1] == round2[1]:
        return 0
    return -1

def send(message):
    print(f"Sending message {message}")
    results = []
    sender = message["sender"]
    for i in range(nodes):
        #Evito un auto_invio
        if i != sender:
            results.append(voters[i].vote(message))

    return results