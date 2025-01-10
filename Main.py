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
        self.mainframe.pack(fill="both", expand=True)
        self.text = ttk.Label(self.mainframe, text="Benvenuto in Paxos Simulator!", background="white")
        self.text.grid(row=0, column=0)
        self.text = ttk.Label(self.mainframe, text="Inserisci il numero di nodi!", background="white")
        self.text.grid(row=1, column=1)
        self.set_text_field = ttk.Entry(self.mainframe)
        self.set_text_field.grid(row=2, column=2)
        self.set_text_button = ttk.Button(self.mainframe, text="Inserisci il numero di nodi", command=lambda: asyncio.run(self.run_paxos()))
        self.set_text_button.grid(row=3, column=2)
        self.root.mainloop()

    async def run_paxos(self):
        nodes = int(self.set_text_field.get())
        async with asyncio.TaskGroup() as tg:
            tg.create_task(Paxos.run_paxos(nodes))


if __name__ == "__main__":
    App()