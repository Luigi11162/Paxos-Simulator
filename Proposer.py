from Utils import send, create_message, MessageTypeProposer
import asyncio


class Proposer:
    def __init__(self, i, my_propose):
        self.i = i
        self.my_propose = my_propose
        self.counter = 1

    def init_round(self, majority, time_max=100000):
        self.counter += 1
        r = (self.counter, self.i)
        last, self.counter = self._send_propose(r)
        v = max(last)
        if not v:
            v = self.my_propose
        self._send_begin(r, v)
        if self.receive_votes(r, majority, time_max):
            self._choose(v, r)
            self._send_success(v)
            self.receive_ack()

    async def _send_propose(self, r):
        message = create_message(MessageTypeProposer.PROPOSE, self.i, values={"r", r})
        await send(message)
        await asyncio.sleep(1)

    def _send_begin(self, r, v):
        message = create_message(MessageTypeProposer.BEGIN, self.i, values={"r": r, "v": v})
        send(message)

    def _send_success(self, v):
        message = create_message(MessageTypeProposer.SUCCESS, self.i, values={"v", v})
        send(message)

    def _choose(self, v, r):
        return

