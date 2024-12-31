class Proposer:
    def __init__(self, i, my_propose):
        self.i = i
        self.my_propose = my_propose
        self.counter = 1

    def init_round(self, majority, time_max):
        self.counter += 1
        wait_voters = 0
        last = []
        r = (self.counter, self.i)
        send_propose(r)
        time = 0
        while wait_voters <= majority:
            last.append(receive_proposes())
            counter = max(last)
            wait_voters += 1
            if time <= time_max:
                break
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


def send_propose(r):
    message = (r, "Propose")


def send_success(v):
    message = (v, "Success")


def receive_proposes():
    return


def receive_ack():
    return


def receive_votes(r):
    return


def choose(v, r):
    return
