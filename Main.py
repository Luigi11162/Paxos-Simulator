import time
from random import randint
from Proposer import Proposer
from Util import choose_proposer
from Voter import Voter


nodes = 5
values = [1, 2, 3, 4, 5]
proposers = []
voters = []


#Istanzio le classi dei Voter e dei Proposer con i valori di partenza
for i in range(nodes):
    proposers.append(Proposer(i, values[i]))
    voters.append(Voter(i, values[i]))


while True:
    i = choose_proposer(nodes)
    proposers[i].init_round(int(nodes / 2))
    time.sleep(randint(10,100))