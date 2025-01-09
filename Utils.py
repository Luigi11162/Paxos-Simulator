import asyncio
import socket
from random import randint
from enum import Enum

nodes = 5
values = [1, 2, 3, 4, 5]
proposers = []
voters = []
HOST = "127.0.0.1"
PORT = 5000

class MessageTypeVoter(Enum):
    OLD_ROUND = 0
    LAST_ROUND = 1
    ACCEPT = 2
    ACK = 3


class MessageTypeProposer(Enum):
    COLLECT = 0
    BEGIN = 1
    SUCCESS = 2


def create_message(message_type, id_sender, message_values=None):
    return {"type": message_type, "sender": id_sender, "values": message_values}


def choose_proposer(n):
    return randint(0, n - 1)


def compare_rounds(round1, round2):
    if round1[0] > round2[0] or round1[0] == round2[0] and round1[1] > round2[1]:
        return 1
    if round1[0] == round2[0] and round1[1] == round2[1]:
        return 0
    return -1


async def send(message):
    results = []
    sender = message["sender"]
    for i in range(nodes):
        #Evito un auto_invio
        if i != sender:
            await send_message_socket(message, i)

    return results


async def initialize_server(index, backlog=nodes):
    try:
        server = await asyncio.start_server(handle_client, HOST, PORT + index)
        print("Server",index,"Inizializzato. In ascolto...")
        async with server:
            await server.serve_forever()
    except socket.error as errore:
        print(f"Qualcosa è andato storto... \n{errore}")
        print("Sto tentando di reinizializzare il server...")
        await initialize_server(index, backlog)

async def send_message_socket(message, index):
    try:
        reader, writer = await asyncio.open_connection(HOST, PORT + index)
        print(f"Invio messaggio {message} a nodo {index}")
        writer.write(message.encode())
        print(f"Invio completato a nodo {index}")
        await writer.drain()
        print(f"Invio completato a nodo {index}")

        data = await reader.read(100)
        writer.close()
        return data
    except socket.error as errore:
        print(f"Qualcosa è andato storto con nodo {index}... \n{errore}")

async def handle_client(reader, writer):
    addr = writer.get_extra_info("peername")
    print(f"Connessione da {addr}")
    data = await reader.read()
    print(f"Ricevuto {data} da {addr}")
    index, result = data
    message = voters[index].vote(result)
    writer.write(message)
    await writer.drain()
    print(f"Inviato {message} a {addr}")
    writer.close()