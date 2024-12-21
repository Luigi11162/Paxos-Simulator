i = None
last_r = (0, i)
last_v = input_i
commit = (0, i)


def vote(message):
    r = message["r"]
    if message["type"] == "Collect":
        if r >= commit:
            send(r, last, last_r, last_v)
            commit = r
        else:
            send(r, old_round, commit)

    if message["type"] == "Begin":
        v= message["v"]
        if r >= commit:
            send_accept(r)
            last_r = r
            last_v = v
        else:
            send_old_round(r, commit)
