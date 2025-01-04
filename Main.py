import time
from random import randint
from Proposer import Proposer
from Utils import choose_proposer, nodes, values, proposers, voters
from Voter import Voter

#Istanzio le classi dei Voter e dei Proposer con i valori di partenza
for i in range(nodes):
    proposers.append(Proposer(i, values[i]))
    voters.append(Voter(i, values[i]))


while True:
    i = choose_proposer(nodes)
    #Arrotonda per eccesso il numero di votanti
    proposers[i].init_round((nodes + 1) // 2)
    time.sleep(randint(10, 20))