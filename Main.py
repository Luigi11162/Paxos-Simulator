import asyncio
import time
from random import randint
from Proposer import Proposer
from Utils import choose_proposer, nodes, values, proposers, voters, initialize_server
from Voter import Voter


async def main():
    #Istanzio le classi dei Voter e dei Proposer con i valori di partenza
    async with asyncio.TaskGroup() as tg:
        for i in range(nodes):
            print(f"Creating voter {i}")
            proposers.append(Proposer(i, values[i]))
            voters.append(Voter(i, values[i]))
            tg.create_task(initialize_server(i))

    while True:
        i = choose_proposer(nodes)
        #Arrotonda per eccesso il numero di votanti

        proposers[i].init_round((nodes + 1) // 2)

        time.sleep(randint(10, 20))

if __name__ == '__main__':
    asyncio.run(main())