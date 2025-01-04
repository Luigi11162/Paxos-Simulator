from Utils import MessageTypeVoter, MessageTypeProposer, create_message, compare_rounds

class Voter:
    def __init__(self, i, last_v):
        self.i = i
        self.last_r = (0, i)
        self.last_v = last_v
        self.commit = (0, i)
        
    def vote(self, message):

        if message["type"] == MessageTypeProposer.COLLECT:
            r = message["values"]["r"]
            if compare_rounds(r, self.commit)>=0:
                self.commit = r
                return self._send_last(r, self.last_r, self.last_v)
            else:
                return self._send_old_round(r, self.commit)

        if message["type"] == MessageTypeProposer.BEGIN:
            r = message["values"]["r"]
            v = message["values"]["v"]
            if compare_rounds(r, self.commit)>=0:
                self.last_r = r
                self.last_v = v
                return self._send_accept(r)
            else:
                return self._send_old_round(r, self.commit)
        if message["type"] == MessageTypeProposer.SUCCESS:
            return self._send_ack()


    def _send_last(self, r, last_r, last_v):
        values = {"r": r, "last_r": last_r, "last_v": last_v}
        return create_message(MessageTypeVoter.LAST_ROUND, self.i, values)

    def _send_old_round(self, r, commit):
        values = {"r": r, "commit": commit}
        return create_message(MessageTypeVoter.OLD_ROUND, self.i, values)

    def _send_accept(self, r):
        values = {"r": r}
        return create_message(MessageTypeVoter.ACCEPT, self.i, values)

    def _send_ack(self):
        return create_message(MessageTypeVoter.ACK, self.i)