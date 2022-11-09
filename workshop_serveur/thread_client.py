import socket
from threading import Thread
from typing import Dict, Tuple

from logger.log import Log
from instruction.instruction import Instruction, Achat, Vente

dict_instruction: Dict[str, Instruction] = \
    {
        "achat": Achat,
        "vente": Vente,
    }


class Client(Thread):

    all: Dict[Tuple[str, int], "Client"] = {}
    states_addr: Dict[str, Tuple[str, int]] = {}

    def __init__(self, sock: socket.socket, addr: Tuple[str, int]):
        Thread.__init__(self)
        self.state = None
        self.sock = sock
        self.addr = addr

        Client.all[addr] = self

    def run(self) -> None:
        self.init_state()
        while True:
            data = self.wait_instruction()
            if not data:
                break
            self.do_instruction(data)
        self.close()

    def wait_instruction(self) -> str:
        return self.sock.recv(2048).decode('utf-8')

    def do_instruction(self, data: str) -> None:
        instruction_type, montant = data.split(':')
        dict_instruction[instruction_type].create(self, montant)

    @classmethod
    @property
    def ClientThread(cls):
        return len(cls.all)

    def init_state(self):
        self.state = self.sock.recv(3).decode("utf-8")
        if self.state in Client.states_addr:
            Log.log("Connection refusé: pays déjà connecté")
            self.close(True)
            return
        Log.log(f"Pays de connection: {self.state}")
        Client.states_addr[self.state] = self.addr

    def close(self, without_state_addr: bool = False):
        self.sock.close()
        Client.all.pop(self.addr)
        if not without_state_addr:
            Client.states_addr.pop(self.state)
        print(f"Connection closed from {self.state}: {self.addr[0]}:{self.addr[1]}")
