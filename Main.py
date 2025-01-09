import asyncio
from random import randint

from Config import nodes, proposers, values, voters
from Proposer import Proposer
from Utils import choose_proposer
from Voter import Voter


async def main():
    #Istanzio le classi dei Voter e dei Proposer con i valori di partenza
    async with asyncio.TaskGroup() as tg:
        for i in range(nodes):
            print(f"Creo il nodo {i}")
            proposers.append(Proposer(i, values[i]))
            voters.append(Voter(i, values[i]))
            tg.create_task(voters[i].initialize_server(i))


        while True:
            await asyncio.sleep(randint(2, 10))
            i = choose_proposer(nodes)
            #Arrotonda per eccesso il numero di votanti
            print(f"Scelgo il proposer {i}")
            tg.create_task(proposers[i].init_round((nodes + 1) // 2))


if __name__ == '__main__':
    asyncio.run(main())