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
            self.counter, propose = last
            if propose is not None:
                self.my_propose = propose
            return

        if message_type == MessageTypeVoter.LAST_ROUND:
            _, propose = last
            if propose is not None:
                self.my_propose = propose

        if self._send_begin(r, self.my_propose)>=majority:
            if self._send_success(last)>=majority:
                print("Value decided: ", self.i, self.my_propose)
                return

        print("Value not decided", self.i, self.my_propose)

    def _send_collect(self, r):
        message = create_message(MessageTypeProposer.COLLECT, self.i, {"r": r})
        results = send(message)
        last = (self.counter, self.i)

        for i in range(len(results)):
            if (results[i]["type"] == MessageTypeVoter.OLD_ROUND and
                    compare_rounds(results[i]["values"]["r"],r)==0 and
                    compare_rounds(results[i]["values"]["commit"], last)>=0):
                    last = (MessageTypeVoter.OLD_ROUND, (results[i]["values"]["r"], results[i]["values"]["commit"]))

        if compare_rounds(last, (self.counter, self.i)) > 0:
            return last

        for i in range(len(results)):
            if results[i]["type"] == MessageTypeVoter.LAST_ROUND:
                if compare_rounds(results[i]["values"]["r"], last) > 0:
                    last = (MessageTypeVoter.OLD_ROUND, (results[i]["values"]["last_r"], results[i]["values"]["last_v"]))

        return last

    def _send_begin(self, r, v):
        message = create_message(MessageTypeProposer.BEGIN, self.i, {"r": r, "v": v})
        results = send(message)

        num_accept = 0
        for i in range(len(results)):
            if results[i]["type"] == MessageTypeVoter.ACCEPT:
                if compare_rounds(results[i]["values"]["r"], r) == 0:
                    num_accept+=1
        return num_accept

    def _send_success(self, v):
        message = create_message(MessageTypeProposer.SUCCESS, self.i, {"v": v})
        results = send(message)
        num_ack = 0
        for i in range(len(results)):
            if results[i]["type"] == MessageTypeVoter.ACK:
                num_ack+=1

        return num_ack

