from Utils import MessageTypeVoter, MessageTypeProposer, create_message, send

class Voter:
    def __init__(self, i, last_v):
        self.i = i
        self.last_r = (0, i)
        self.last_v = last_v
        self.commit = (0, i)

    def vote(self, message):
        r = message["r"]
        if message["type"] == MessageTypeProposer.PROPOSE:
            if r >= self.commit:
                self._send_last(r, self.last_r, self.last_v)
                self.commit = r
            else:
                self._send_old_round(r, self.commit)

        if message["type"] == MessageTypeProposer.BEGIN:
            v = message["v"]
            if r >= self.commit:
                self._send_accept(r)
                self.last_r = r
                self.last_v = v
            else:
                self._send_old_round(r, self.commit)
        if message["type"] == MessageTypeProposer.SUCCESS:
            self._send_ack()


    def _send_accept(self, r):
        message = create_message(MessageTypeVoter.ACCEPT, self.i, r)
        send(message)


    def _send_old_round(self, r, commit):
        values = {"r": r, "commit": commit}
        message = create_message(MessageTypeVoter.OLD_ROUND, self.i, values)
        send(message)


    def _send_last(self, r, last_r, last_v):
        message = create_message( MessageTypeVoter.LAST_ROUND,self.i, r, last_r, last_v)
        send(message)

    def _send_ack(self):
        message = (MessageTypeVoter.ACK, self.i)
        send(message)


