import asyncio
import tkinter as tk
from tkinter import ttk

import Paxos

class App:
    def __init__(self):
        self.button_start = None
        self.root = tk.Tk()
        self.root.title("Paxos Simulator")
        self.root.geometry("800x600")
        self.mainframe = tk.Frame(self.root, background="white")
        self.mainframe.pack(fill="both", expand=True, padx=10, pady=10)

        self.welcome_label = ttk.Label(self.mainframe, text="Benvenuto in Paxos Simulator!", background="white")
        self.welcome_label.grid(row=0, column=0, padx=300, pady=10)

        self.input_label = ttk.Label(self.mainframe, text="Inserisci il numero di nodi:", background="white")
        self.input_label.grid(row=1, column=0, pady=5)

        self.set_text_field = ttk.Entry(self.mainframe)
        self.set_text_field.grid(row=2, column=0, pady=5)

        self.button_set_nodes = ttk.Button(self.mainframe, text="Conferma", command=self.confirm_nodes)
        self.button_set_nodes.grid(row=3, column=0, pady=10)

        self.button_stop = ttk.Button(self.mainframe, text="Ferma", command=Paxos.stop_paxos)
        self.button_stop.grid(row=4, column=0, pady=10)

        self.invalid_number_label = ttk.Label(self.mainframe, text="Inserire un numero valido", foreground="red", background="white")
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
            if self.button_start is not None : self.button_start.grid_remove()
            self.set_values = []
            nodes = int(self.set_text_field.get())
            for i in range(nodes):
                self.set_values.append((ttk.Label(self.mainframe, text=f"Inserisci il valore del nodo {i}:", background="white"), ttk.Entry(self.mainframe)))
                self.set_values[i][0].grid(row=5 + 2*i, column=0, pady=5)
                self.set_values[i][1].grid(row=5 + 2*i+1, column=0, pady=5)
            self.button_start = ttk.Button(self.mainframe, text="Avvia", command = lambda: self.run_paxos(nodes))
            self.button_start.grid(row=5 + 2*nodes, column=0, pady=10)

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
                self.invalid_number_label.grid(row=5 + 2 * i + 1, column=1, pady=5)
                return
        asyncio.create_task(Paxos.run_paxos(nodes, values))


if __name__ == "__main__":
    asyncio.run(App().update_tkinter())
