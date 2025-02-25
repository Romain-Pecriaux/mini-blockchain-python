import hashlib
import json
import time

class Block:
    def __init__(self, index, previous_hash, data, timestamp=None):
        self.index = index
        self.previous_hash = previous_hash
        self.data = data
        self.timestamp = timestamp or time.time()
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """
        Calcule le hash du bloc en utilisant SHA-256.
        """
        block_string = f"{self.index}{self.previous_hash}{self.data}{self.timestamp}".encode()
        return hashlib.sha256(block_string).hexdigest()

    def to_dict(self):
        """
        Convertit le bloc en dictionnaire pour le stockage JSON.
        """
        return {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "data": self.data,
            "timestamp": self.timestamp,
            "hash": self.hash
        }

    @staticmethod
    def from_dict(block_dict):
        """
        Crée un objet Block à partir d'un dictionnaire.
        """
        return Block(
            block_dict["index"],
            block_dict["previous_hash"],
            block_dict["data"],
            block_dict["timestamp"]
        )



class Blockchain:
    def __init__(self):
        self.chain = []
        self.load_chain()  # Charger depuis JSON si dispo, sinon créer le bloc genesis

    def create_genesis_block(self):
        """
        Crée le premier bloc de la blockchain (bloc génésis).
        """
        return Block(0, "0", "Genesis Block")

    def add_block(self, data):
        """
        Ajoute un nouveau bloc à la blockchain.
        """
        last_block = self.chain[-1]
        new_block = Block(len(self.chain), last_block.hash, data)
        self.chain.append(new_block)
        self.save_chain()

    def is_valid_chain(self):
        """
        Vérifie l'intégrité de la blockchain.
        """
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            
            # Vérification du hash précédent
            if current.previous_hash != previous.hash:
                return False
            
            # Vérification du hash du bloc
            if current.hash != current.calculate_hash():
                return False

        return True

    def save_chain(self, filename="blockchain.json"):
        """
        Sauvegarde la blockchain dans un fichier JSON.
        """
        with open(filename, "w") as f:
            json.dump([block.to_dict() for block in self.chain], f, indent=4)

    def load_chain(self, filename="blockchain.json"):
        """
        Charge la blockchain depuis un fichier JSON.
        """
        try:
            with open(filename, "r") as f:
                blocks = json.load(f)
                self.chain = [Block.from_dict(b) for b in blocks]
        except (FileNotFoundError, json.JSONDecodeError):
            print("Aucune blockchain trouvée, création d'un bloc génésis.")
            self.chain = [self.create_genesis_block()]
            self.save_chain()