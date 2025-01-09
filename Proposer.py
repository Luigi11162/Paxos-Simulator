import asyncio
import pickle
import socket
from Utils import create_message, compare_rounds
from Config import MessageTypeProposer, MessageTypeVoter, HOST, PORT, nodes


class Proposer:
    def __init__(self, i, my_propose):
        self.i = i
        self.my_propose = my_propose
        self.counter = 0


    async def init_round(self, majority):
        self.counter += 1
        r = (self.counter, self.i)
        num_last, propose = await self._send_collect(r)

        if num_last < majority:
            return

        if propose is not None:
            self.my_propose = propose

        if await self._send_begin(r, self.my_propose)>=majority:
            if await self._send_success(self.my_propose)>=majority:
                print(f"Valore deciso: {self.my_propose} al round: {r}")
                return True

        print("Valore non deciso", self.i, self.my_propose)

    async def _send_collect(self, r):
        message = create_message(MessageTypeProposer.COLLECT, self.i, {"r": r})
        results = await self.send(message)
        last = (self.counter, self.i)
        propose = self.my_propose
        num_last = 0
        for i in range(len(results)):
            if results[i]["type"] == MessageTypeVoter.LAST_ROUND:
                num_last+=1
                if compare_rounds(results[i]["values"]["r"], last) > 0:
                    last =  results[i]["values"]["r"]
                    propose = results[i]["values"]["last_v"]

        return num_last, propose

    async def _send_begin(self, r, v):
        message = create_message(MessageTypeProposer.BEGIN, self.i,{"r": r, "v": v})
        results = await self.send(message)

        num_accept = 0
        for i in range(len(results)):
            if results[i]["type"] == MessageTypeVoter.ACCEPT:
                if compare_rounds(results[i]["values"]["r"], r) == 0:
                    num_accept+=1

        return num_accept

    async def _send_success(self, v):
        message = create_message(MessageTypeProposer.SUCCESS, self.i, {"v": v})
        results = await self.send(message)
        num_ack = 0
        for i in range(len(results)):
            if results[i]["type"] == MessageTypeVoter.ACK:
                num_ack+=1

        return num_ack

    async def send(self,message):
        results = []
        encoded_message = pickle.dumps(message)
        for i in range(nodes):
            #Evito un auto_invio
            if i != self.i:
                try:
                    reader, writer = await asyncio.open_connection(HOST, PORT + i)
                    print(f"Invio messaggio {message} a nodo {i}")
                    writer.write(encoded_message)
                    await writer.drain()
                    print(f"Invio completato a nodo {i}")

                    data = await reader.read(1000)
                    data = pickle.loads(data)
                    print(f"Ricevuti messaggi: {data}")
                    writer.close()
                    await writer.wait_closed()
                    results.append(data)
                except socket.error as errore:
                    print(f"Qualcosa è andato storto con nodo {i}... \n{errore}")

        return results