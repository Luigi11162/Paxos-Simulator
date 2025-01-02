import time
from random import randint
from Proposer import Proposer
from Util import choose_proposer
from Voter import Voter


nodes = 5
values = [1, 2, 3, 4, 5]
proposer = []
voter = []


#Imposto le classi dei Voter e Proposer con i valori di partenza
for i in range(nodes):
    proposer.append(Proposer(i, values[i]))
    voter.append(Voter(i, values[i]))


while True:
    i = choose_proposer(nodes)
    proposer[i].init_round(int(nodes/2))
    time.sleep(randint(10,100))