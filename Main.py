import asyncio
import tkinter as tk
from asyncio import TaskGroup
from tkinter import ttk

import Paxos


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Paxos Simulator")
        self.root.geometry("800x600")
        self.mainframe = tk.Frame(self.root, background="white")
        self.mainframe.pack(fill="both", expand=True, padx=10, pady=10)

        self.welcome_label = ttk.Label(self.mainframe, text="Benvenuto in Paxos Simulator!", background="white")
        self.welcome_label.grid(row=0, column=0, columnspan=2, padx=300, pady=10)

        self.input_label = ttk.Label(self.mainframe, text="Inserisci il numero di nodi:", background="white")
        self.input_label.grid(row=1, column=0, sticky="e", pady=5)

        self.set_text_field = ttk.Entry(self.mainframe)
        self.set_text_field.grid(row=2, column=0, sticky="e", pady=5)

        self.set_text_button = ttk.Button(self.mainframe, text="Avvia", command=self.run)
        self.set_text_button.grid(row=3, column=0, columnspan=2, pady=10)

        asyncio.run(self.mainloop())

    async def mainloop(self):
        async with TaskGroup() as tg:
            tg.create_task(self.root.mainloop())

    def run(self):
        asyncio.get_running_loop().cancel()
        #self.run_paxos()

    async def run_paxos(self):
        nodes = int(self.set_text_field.get())
        async with TaskGroup() as tg:
            tg.create_task(Paxos.run_paxos(nodes))


if __name__ == "__main__":
    App()