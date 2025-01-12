from random import randint


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
