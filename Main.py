import time
from random import randint
from Proposer import Proposer
from Voter import Voter


nodes = 5
values = [1, 2, 3, 4, 5]
proposer = []
voter = []

def choose_proposer():
    return randint(0,nodes-1)

#Imposto le classi dei Voter e Proposer con i valori di partenza
for i in range(nodes):
    proposer.append(Proposer(i, values[i]))
    voter.append(Voter(i, values[i]))


while True:
    i = choose_proposer()
    proposer[i].init_round(int(nodes/2))
    time.sleep(randint(10,100))