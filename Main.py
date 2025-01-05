import asyncio
import time
from random import randint
from Proposer import Proposer
from Utils import choose_proposer, nodes, values, proposers, voters, initialize_server
from Voter import Voter


async def main():
    #Istanzio le classi dei Voter e dei Proposer con i valori di partenza
    for i in range(nodes):
        proposers.append(Proposer(i, values[i]))
        voters.append(Voter(i, values[i]))
        await initialize_server(i)

    while True:
        i = choose_proposer(nodes)
        #Arrotonda per eccesso il numero di votanti

        await proposers[i].init_round((nodes + 1) // 2)

        time.sleep(randint(10, 20))

asyncio.run(main())