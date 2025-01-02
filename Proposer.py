import time

from Util import send
import asyncio

class Proposer:
    def __init__(self, i, my_propose):
        self.i = i
        self.my_propose = my_propose
        self.counter = 1


    def init_round(self, majority, time_max=100000):
        self.counter += 1
        r = (self.counter, self.i)
        send_propose(r)
        last, self.counter = receive_proposes(majority, time_max)
        v = max(last)
        if not v:
            v = self.my_propose
        send_begin(r, v)
        if  receive_votes(r, majority, time_max):
            choose(v, r)
            send_success(v)
            receive_ack()

def send_begin(r, v):
    message = (r, v, "Begin")
    send(message)


def send_propose(r):
    message = (r, "Propose")
    send(message)


def send_success(v):
    message = (v, "Success")
    send(message)


def receive_proposes(majority, time_max):
    result = wait_voters(majority, time_max, "receive_proposes")
    last, counter = result
    return last, counter


def receive_ack():
    return


def receive_votes(r, majority, time_max):
    result = wait_voters(majority, time_max, "receive_votes")
    num_votes = 0
    for vote in result:
        if vote == r:
            num_votes +=1
    if num_votes >= majority:
        return True
    return False


def choose(v, r):
    return

def wait_voters(majority, time_max, function):
    voters = 0
    result = []
    while voters <= majority:
        result.append(asyncio.wait_for(function, time_max))
        voters += 1
    return result