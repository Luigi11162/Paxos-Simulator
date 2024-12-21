counter = 1
my_propose = None
i = None


def init_round():
    global counter
    counter += 1
    wait_voters = 0
    last = []
    r = (counter, i)
    send_propose(r)
    while wait_voters <= majority:
        last.append(receive_proposes(r, last, new_r, v))
        counter = max_counter
        wait_voters += 1
        if time <= time_max:
            break
    v = max(last)
    if not v:
        v = my_propose
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
