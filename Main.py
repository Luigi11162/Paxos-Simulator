import asyncio
import tkinter as tk
from tkinter import ttk

import Paxos
from Voter import Voter
from Proposer import Proposer
from Config import MessageTypeVoter, voters, proposers, MessageTypeProposer


class App:
    BACKGROUND = "#f7f7f7"
    COL_WIDTH = 100
    ROW_HEIGHT = 20

    def __init__(self):
        super().__init__()
        self.button_start = None
        self.root = tk.Tk()
        self.root.title("Paxos Simulator")
        self.root.geometry("1200x600")
        self.root.configure(bg=self.BACKGROUND)

        self.mainframe = tk.Frame(self.root, background=self.BACKGROUND)
        self.mainframe.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.simulation_canvas = tk.Canvas(self.mainframe, bg="white", width=700, height=400)
        self.simulation_canvas.grid(row=0, column=1, rowspan=10, padx=20, pady=20)

        self.position_row = 1

        self.welcome_label = ttk.Label(self.mainframe, text="Benvenuto in Paxos Simulator!", background=self.BACKGROUND,
                                       font=("Helvetica", 18, "bold"), anchor="center")
        self.welcome_label.grid(row=0, column=0, pady=20)

        self.input_label = ttk.Label(self.mainframe, text="Inserisci il numero di nodi:", background=self.BACKGROUND,
                                     font=("Helvetica", 12))
        self.input_label.grid(row=1, column=0, pady=10)

        self.set_text_field = ttk.Entry(self.mainframe, font=("Helvetica", 12))
        self.set_text_field.grid(row=2, column=0, pady=5)

        self.button_set_nodes = ttk.Button(self.mainframe, text="Conferma", command=self.confirm_nodes)
        self.button_set_nodes.grid(row=3, column=0, pady=10)

        self.button_stop = ttk.Button(self.mainframe, text="Ferma", command=Paxos.stop_paxos)
        self.button_stop.grid(row=4, column=0, pady=10)

        self.invalid_number_label = ttk.Label(self.mainframe, text="Inserire un numero valido", foreground="red",
                                              background=self.BACKGROUND, font=("Helvetica", 10))
        self.set_values = []

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.running = True
        asyncio.set_event_loop(asyncio.new_event_loop())
        asyncio.run(self.update_tkinter())

    def on_close(self):
        self.running = False
        self.root.destroy()

    async def update_tkinter(self):
        while self.running:
            self.root.update()
            await asyncio.sleep(0.01)

    def confirm_nodes(self):
        try:
            self.invalid_number_label.grid_remove()
            [[x[i].grid_remove() for i in range(len(x))] for x in self.set_values]
            if self.button_start is not None: self.button_start.grid_remove()
            self.set_values = []
            nodes = int(self.set_text_field.get())
            for i in range(nodes):
                self.set_values.append((ttk.Label(self.mainframe, text=f"Inserisci il valore del nodo {i}:",
                                                  background=self.BACKGROUND),
                                        ttk.Entry(self.mainframe, font=("Helvetica", 12))))
                self.set_values[i][0].grid(row=5 + 2 * i, column=0, pady=5, sticky="w")
                self.set_values[i][1].grid(row=5 + 2 * i + 1, column=0, pady=5)
            self.button_start = ttk.Button(self.mainframe, text="Avvia", command=lambda: self.run_paxos(nodes))
            self.button_start.grid(row=5 + 2 * nodes, column=0, pady=10)
        except ValueError:
            self.invalid_number_label.grid(row=5, column=0, pady=5)
            return

    def run_paxos(self, nodes):
        values = []
        self.invalid_number_label.grid_remove()
        for i in range(len(self.set_values)):
            try:
                values.append(int(self.set_values[i][1].get()))
            except ValueError:
                self.invalid_number_label.grid(row=5 + 2 * i + 1, column=0, pady=5)
                return

        self.draw_simulation(nodes)
        for i in range(nodes):
            proposers.append(Proposer(i, values[i]))
            proposers[i].attach(self)
            voters.append(Voter(i, values[i]))
            voters[i].attach(proposers[i])
            voters[i].attach(self)
        asyncio.create_task(Paxos.run_paxos(nodes))


    def draw_simulation(self, nodes):

        headers = ["Numero round", "Valore"] + [i for i in range(nodes)]
        for i, header in enumerate(headers):
            self.simulation_canvas.create_text((i + 0.5) * self.COL_WIDTH, 20, text=header, font=("Arial", 10, "bold"))

    def draw_propose(self, node, num_round, value, message_type):
        match message_type:
            case MessageTypeProposer.COLLECT:
                self.position_row +=1

            case MessageTypeProposer.BEGIN:
                self.simulation_canvas.create_text(0.5 * self.COL_WIDTH, self.ROW_HEIGHT*self.position_row+self.ROW_HEIGHT/2 , text=f"{num_round}", font=("Arial", 10, "bold"))
                self.simulation_canvas.create_text(1.5 * self.COL_WIDTH, self.ROW_HEIGHT*self.position_row+self.ROW_HEIGHT/2, text=value, font=("Arial", 10, "bold"))

                x1, y1 = (2.5+node) * self.COL_WIDTH, self.ROW_HEIGHT*self.position_row-self.ROW_HEIGHT/2
                x2, y2 = (2.5+node) * self.COL_WIDTH, self.ROW_HEIGHT*self.position_row
                self.simulation_canvas.create_line(x1, y1, x2, y2, width=2)

    def draw_vote(self, message_type, node):
        match message_type:
            case MessageTypeVoter.LAST_ROUND:
                self.simulation_canvas.create_rectangle((2.5+node)*self.COL_WIDTH-10, self.ROW_HEIGHT*self.position_row, (2.5+node)*self.COL_WIDTH+10, self.ROW_HEIGHT*self.position_row+10, fill="blue")
            case MessageTypeVoter.ACCEPT:
                self.simulation_canvas.create_oval((2.5+node)*self.COL_WIDTH-10, self.ROW_HEIGHT*self.position_row, (2.5+node)*self.COL_WIDTH+10, self.ROW_HEIGHT*self.position_row+10, fill="red")

    def update(self, subject):
        if isinstance(subject, Voter):
            self.draw_vote(subject.message_type, subject.i)
        elif isinstance(subject, Proposer):
            self.draw_propose(subject.i, subject.r, subject.my_propose, subject.message_type)

if __name__ == "__main__":
    asyncio.run(App().update_tkinter())
