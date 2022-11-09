from abc import ABC, abstractmethod
from typing import Dict
from logger.log import Log


class Instruction(ABC):

    @staticmethod
    @abstractmethod
    def create(client, data):
        pass


class Achat(Instruction):

    all: Dict[id, "Achat"] = {}

    def __init__(self, client: "Client", data: str):
        self.client = client
        self.ville = client.state
        self.montant = int(data)

        Log.log(f"Achat {id(self)} crée par {self.ville}, d'un montant de {self.montant} kwh")
        insert = self.__check_vente()
        if insert:
            Achat.all[id(self)] = self

    @staticmethod
    def create(client, data):
        achat = Achat(client, data)
        return achat if id(achat) in Achat.all else None

    def __check_vente(self):
        for id_vente, vente in Vente.all.items():
            montant_acheter = vente.envoie_energie(self)
            self.montant -= montant_acheter
            self.client.sock.send(f"achat:{id(self)}>{id(vente)} {vente.ville} {montant_acheter}".encode("utf-8"))
            if self.montant <= 0:
                return False
        return True

    def prendre_energie(self, vente: "Vente"):
        montant_pris = min(self.montant, vente.montant)
        self.montant -= montant_pris
        self.client.sock.send(f"achat:{id(self)}>{id(vente)} {vente.ville} {montant_pris}".encode("utf-8"))
        Log.log(f"Achat effectué: {montant_pris} kwh achété par {self.ville} à {vente.ville}")
        if self.montant <= 0:
            self.close()
        return montant_pris

    def close(self):
        Log.log(f"Achat {id(self)} fermé")
        Achat.all.pop(id(self))


class Vente(Instruction):

    all: Dict[id, "Vente"] = {}

    def __init__(self, client: "Client", montant: str):
        self.client = client
        self.montant = int(montant)
        self.ville = client.state
        Log.log(f"Vente {id(self)} crée par {self.ville}, d'un montant de {self.montant} kwh")

        insert = self.__check_achat()
        if insert:
            Vente.all[id(self)] = self

    @staticmethod
    def create(client, data):
        vente = Vente(client, data)
        return vente if id(vente) in Vente.all else None

    def __check_achat(self):
        for id_achat, achat in Achat.all.items():
            montant_vendu = achat.prendre_energie(self)
            self.montant -= montant_vendu
            self.client.sock.send(f"vente:{id(self)}>{id(achat)} {achat.ville} {montant_vendu}".encode('utf-8'))
            if self.montant <= 0:
                return False
        return True

    def envoie_energie(self, achat: Achat):
        montant_envoier = min(self.montant, achat.montant)
        self.montant -= montant_envoier
        self.client.sock.send(f"vente:{id(self)}>{id(achat)} {achat.ville} {montant_envoier}".encode("utf-8"))
        Log.log(f"Vente effectué: {montant_envoier} kwh vendu par {self.ville} à {achat.ville}")
        if self.montant <= 0:
            self.close()
        return montant_envoier

    def close(self):
        Log.log(f"Vente {id(self)} fermé")
        Vente.all.pop(id(self))
