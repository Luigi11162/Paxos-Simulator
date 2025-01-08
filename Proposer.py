from Utils import send, create_message, MessageTypeProposer, MessageTypeVoter, compare_rounds


class Proposer:
    def __init__(self, i, my_propose):
        self.i = i
        self.my_propose = my_propose
        self.counter = 1


    def init_round(self, majority):
        self.counter += 1
        r = (self.counter, self.i)
        num_last, propose = self._send_collect(r)

        if num_last < majority:
            return

        if propose is not None:
            self.my_propose = propose

        if self._send_begin(r, self.my_propose)>=majority:
            if self._send_success(self.my_propose)>=majority:
                print("Value decided: ", self.i, self.my_propose)
                return

        print("Value not decided", self.i, self.my_propose)

    def _send_collect(self, r):
        message = create_message(MessageTypeProposer.COLLECT, self.i, {"r": r})
        results = send(message)
        last = (self.counter, self.i)
        propose = self.my_propose
        num_last = 0
        for i in range(len(results)):
            if results[i]["type"] == MessageTypeVoter.LAST_ROUND:
                num_last+=1
                if compare_rounds(results[i]["values"]["r"], last) > 0:
                    last =  results[i]["values"]["r"]
                    propose = results[i]["values"]["last_v"]

        return num_last, propose

    def _send_begin(self, r, v):
        message = create_message(MessageTypeProposer.BEGIN, self.i,{"r": r, "v": v})
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

