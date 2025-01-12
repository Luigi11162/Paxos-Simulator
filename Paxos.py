import asyncio
from random import randint

from Config import proposers, voters
from Utils import choose_proposer

async def run_paxos(num_nodes):
    try:
        #Istanzio le classi dei Voter e dei Proposer con i valori di partenza
        async with asyncio.TaskGroup() as tg:
            for i in range(num_nodes):
                tg.create_task(voters[i].initialize_server(num_nodes))

            while True:

                await asyncio.sleep(randint(2, 10))
                i = choose_proposer(num_nodes)
                #Arrotonda per eccesso il numero di votanti
                print(f"Scelgo il proposer {i}")
                tg.create_task(proposers[i].init_round(num_nodes))
    except KeyboardInterrupt:
        print("Paxos Interrotto!")
        return

def stop_paxos():
    try:
        pass
    except RuntimeError as e:
        print(f"Paxos non ancora inizializzato {e}")
