from Utils import send, create_message, MessageTypeProposer, MessageTypeVoter, compare_rounds


class Proposer:
    def __init__(self, i, my_propose):
        self.i = i
        self.my_propose = my_propose
        self.counter = 1

    def init_round(self, majority):
        self.counter += 1
        r = (self.counter, self.i)
        message_type, last = self._send_collect(r)
        if message_type == MessageTypeVoter.OLD_ROUND:
            self.counter, self.my_propose= last
        else:
            self._choose(last, r)
            self._send_success(last)

    async def _send_collect(self, r):
        message = create_message(MessageTypeProposer.COLLECT, self.i, values={"r", r})
        results = send(message)
        last = (self.counter, self.i)

        for i in range(len(results)):
            if results[i]["type"] == MessageTypeVoter.OLD_ROUND:
                if compare_rounds((results[i]["values"]["r"], results[i]["commit"]), last)>=0:
                    last = (MessageTypeVoter.OLD_ROUND, (results[i]["r"], results[i]["commit"]))

        if compare_rounds(last, (self.counter, self.i)) > 0:
            return last

        for i in range(len(results)):
            if results[i]["type"] == MessageTypeVoter.LAST_ROUND:
                if compare_rounds(results[i]["r"], last) > 0:
                    last = (MessageTypeVoter.OLD_ROUND, (results[i]["last_r"], results[i]["last_v"]))

        return last

    def _send_begin(self, r, v):
        message = create_message(MessageTypeProposer.BEGIN, self.i, values={"r": r, "v": v})
        send(message)

    def _send_success(self, v):
        message = create_message(MessageTypeProposer.SUCCESS, self.i, values={"v", v})
        send(message)

    def _choose(self, v, r):
        return

