from Util import send, create_message, MessageTypeProposer
import asyncio

class Proposer:
    def __init__(self, i, my_propose):
        self.i = i
        self.my_propose = my_propose
        self.counter = 1


    def init_round(self, majority, time_max=100000):
        self.counter += 1
        r = (self.counter, self.i)
        self._send_propose(r)
        last, self.counter = self.receive_proposes(majority, time_max)
        v = max(last)
        if not v:
            v = self.my_propose
        self._send_begin(r, v)
        if  self.receive_votes(r, majority, time_max):
            self.choose(v, r)
            self._send_success(v)
            self.receive_ack()

    def _send_begin(self,r, v):
        message = create_message(MessageTypeProposer.BEGIN, self.i, r, v)
        send(message)


    def _send_propose(self, r):
        message = create_message(MessageTypeProposer.PROPOSE,self.i, r)
        send(message)


    def _send_success(self, v):
        message = create_message(MessageTypeProposer.SUCCESS, self.i, v)
        send(message)


    def receive_proposes (self, majority, time_max):
        result = self._wait_voters(majority, time_max, "receive_proposes")
        last, counter = result
        return last, counter


    def receive_ack(self):
        return


    def receive_votes(self, r, majority, time_max):
        result = self._wait_voters(majority, time_max, "receive_votes")
        num_votes = 0
        for vote in result:
            if vote == r:
                num_votes +=1
        if num_votes >= majority:
            return True
        return False


    def _choose(self, v, r):
        return

    def _wait_voters(self, majority, time_max, function):
        self.voters = 0
        result = []
        while self.voters <= majority:
            result.append(asyncio.wait_for(function, time_max))
            self.voters += 1
        return result