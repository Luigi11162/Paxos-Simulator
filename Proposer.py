from Util import send
import asyncio


class Proposer:
    def __init__(self, i, my_propose):
        self.i = i
        self.my_propose = my_propose
        self.counter = 1

    def init_round(self, majority, time_max):
        self.counter += 1
        r = (self.counter, self.i)
        send_propose(r)
        time = 0
        last, self.counter = receive_proposes(majority, time_max)

        v = max(last)
        if not v:
            v = self.my_propose
        send_begin(r, v)
        wait_voters = 0
        while wait_voters <= majority:
            receive_votes(r)
            wait_voters += 1
            if time <= time_max:
                break
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
    wait_voters = 0
    last = []
    while wait_voters <= majority:
        last.append(asyncio.wait(time_max))
        counter = last
        wait_voters += 1
    return last, counter


def receive_ack():
    return


def receive_votes(r):
    return


def choose(v, r):
    return
