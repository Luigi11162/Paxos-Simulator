class Voter:
    def __init__(self, i, last_v):
        self.i = i
        self.last_r = (0, i)
        self.last_v = last_v
        self.commit = (0, i)

    def vote(self, message):
        r = message["r"]
        if message["type"] == "Collect":
            if r >= self.commit:
                send_last(r, self.last_r, self.last_v)
                self.commit = r
            else:
                send_old_round(r, self.commit)

        if message["type"] == "Begin":
            v = message["v"]
            if r >= self.commit:
                send_accept(r)
                self.last_r = r
                self.last_v = v
            else:
                send_old_round(r, self.commit)


def send(content, round, type=""):
    #TODO implement send function
    pass


def send_accept(r):
    message = (r, "Accept")


def send_old_round(r, commit):
    message = (r, "Old Round", commit)

def send_last(r, last_r, last_v):
    message = (r, "Last Round", last_r, last_v)