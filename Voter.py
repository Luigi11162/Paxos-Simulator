import asyncio
import pickle
import socket
from random import randint

from Observer import Observer
from Utils import create_message, compare_rounds
from Config import HOST, PORT,MessageTypeVoter, MessageTypeProposer

class Voter(Observer):
    def __init__(self, i, last_v):
        super().__init__()
        self._i = i
        self._last_r = (0, i)
        self._last_v = last_v
        self._commit = (0, i)
        self._decision = False

    @property
    def last_r(self):
        return self._last_r

    @last_r.setter
    def last_r(self, value):
        self._last_r = value
        self.notify()

    @property
    def last_v(self):
        return self._last_v

    @last_v.setter
    def last_v(self, value):
        self._last_v = value
        self.notify()

    @property
    def decision(self):
        return self._decision

    @decision.setter
    def decision(self, value):
        self._decision = value
        self.notify()

    def vote(self, message):
        if message["type"] == MessageTypeProposer.COLLECT:
            r = message["values"]["r"]
            if compare_rounds(r, self._commit)>=0:
                self._commit = r
                return self._send_last(r, self._last_r, self._last_v)
            else:
                return self._send_old_round(r, self._commit)

        if message["type"] == MessageTypeProposer.BEGIN:
            r = message["values"]["r"]
            v = message["values"]["v"]
            if compare_rounds(r, self._commit)>=0:
                self.last_r = r
                self.last_v = v
                return self._send_accept(r)
            else:
                return self._send_old_round(r, self._commit)
        if message["type"] == MessageTypeProposer.SUCCESS:
            self.last_v=message["values"]["v"]
            self._decision = True
            return self._send_ack()


    def _send_last(self, r, last_r, last_v):
        values = {"r": r, "last_r": last_r, "last_v": last_v}
        return create_message(MessageTypeVoter.LAST_ROUND, self._i, values)

    def _send_old_round(self, r, commit):
        values = {"r": r, "commit": commit}
        return create_message(MessageTypeVoter.OLD_ROUND, self._i, values)

    def _send_accept(self, r):
        values = {"r": r}
        return create_message(MessageTypeVoter.ACCEPT, self._i, values)

    def _send_ack(self):
        return create_message(MessageTypeVoter.ACK, self._i)

    async def initialize_server(self, backlog=100):
        try:
            server = await asyncio.start_server(self._handle_client, HOST, PORT + self._i)
            print("Server", self._i, "Inizializzato. In ascolto...")
            async with server:
                await server.serve_forever()
        except socket.error as errore:
            print(f"Qualcosa è andato storto al nodo {self._i} ... \n{errore}")
            print("Sto tentando di reinizializzare il server...")
            await self.initialize_server(backlog)


    async def _handle_client(self, reader, writer):
        if randint(0, 3) != 0:
            data = await reader.read(1000)
            data = pickle.loads(data)
            print(f"Connessione dal nodo {data["sender"]}")
            print(f"Ricevuto {data} dal nodo {data["sender"]}")
            result = data
            message = self.vote(result)
            encoded_message = pickle.dumps(message)
            writer.write(encoded_message)
            await writer.drain()
            print(f"Inviato {message} al nodo {data["sender"]}")
            writer.close()
            await writer.wait_closed()
