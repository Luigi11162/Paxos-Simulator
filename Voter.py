import asyncio
import pickle
import socket

from Utils import create_message, compare_rounds
from Config import HOST, PORT,MessageTypeVoter, MessageTypeProposer, nodes

class Voter:
    def __init__(self, i, last_v):
        self.i = i
        self.last_r = (0, i)
        self.last_v = last_v
        self.commit = (0, i)

    def vote(self, message):
        if message["type"] == MessageTypeProposer.COLLECT:
            r = message["values"]["r"]
            if compare_rounds(r, self.commit)>=0:
                self.commit = r
                return self._send_last(r, self.last_r, self.last_v)
            else:
                return self._send_old_round(r, self.commit)

        if message["type"] == MessageTypeProposer.BEGIN:
            r = message["values"]["r"]
            v = message["values"]["v"]
            if compare_rounds(r, self.commit)>=0:
                self.last_r = r
                self.last_v = v
                return self._send_accept(r)
            else:
                return self._send_old_round(r, self.commit)
        if message["type"] == MessageTypeProposer.SUCCESS:
            self.last_v=message["values"]["v"]
            return self._send_ack()


    def _send_last(self, r, last_r, last_v):
        values = {"r": r, "last_r": last_r, "last_v": last_v}
        return create_message(MessageTypeVoter.LAST_ROUND, self.i, values)

    def _send_old_round(self, r, commit):
        values = {"r": r, "commit": commit}
        return create_message(MessageTypeVoter.OLD_ROUND, self.i, values)

    def _send_accept(self, r):
        values = {"r": r}
        return create_message(MessageTypeVoter.ACCEPT, self.i, values)

    def _send_ack(self):
        return create_message(MessageTypeVoter.ACK, self.i)

    async def initialize_server(self, backlog=nodes):
        try:
            server = await asyncio.start_server(self.handle_client, HOST, PORT + self.i)
            print("Server", self.i, "Inizializzato. In ascolto...")
            async with server:
                await server.serve_forever()
        except socket.error as errore:
            print(f"Qualcosa è andato storto... \n{errore}")
            print("Sto tentando di reinizializzare il server...")
            await self.initialize_server(backlog)


    async def handle_client(self, reader, writer):
        data = await reader.read(1000)
        data = pickle.loads(data)
        addr = writer.get_extra_info("peername")
        print(f"Connessione da {addr}")
        print(f"Ricevuto {data} da {addr}")
        result = data
        message = self.vote(result)
        encoded_message = pickle.dumps(message)
        writer.write(encoded_message)
        await writer.drain()
        print(f"Inviato {message} a {addr}")
        writer.close()
        await writer.wait_closed()