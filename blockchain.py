import hashlib
import json
import time

class Block:
    def __init__(self, index, previous_hash, transactions, timestamp=None):
        """
        Initialise un nouveau bloc.
        :param index: Index du bloc.
        :param previous_hash: Hash du bloc précédent.
        :param transactions: Liste des transactions.
        :param timestamp: Timestamp du bloc.
        """
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions  # Liste de transactions
        self.timestamp = timestamp or time.time()
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """
        Calcule le hash du bloc en utilisant SHA-256.
        """
        block_string = f"{self.index}{self.previous_hash}{self.transactions}{self.timestamp}{self.nonce}".encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        """
        Mine le bloc en trouvant un nonce qui satisfait la difficulté.
        """
        pattern = '0' * difficulty
        while not self.hash.startswith(pattern):
            self.nonce += 1
            self.hash = self.calculate_hash()

    def to_dict(self):
        """
        Convertit le bloc en dictionnaire pour le stockage JSON.
        """
        return {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "transactions": [t.__dict__ for t in self.transactions],  # Convertir les transactions en dictionnaires
            "timestamp": self.timestamp,
            "nonce": self.nonce,
            "hash": self.hash
        }

    @staticmethod
    def from_dict(block_dict):
        """
        Crée un objet Block à partir d'un dictionnaire.
        """
        transactions = [Transaction(**t) for t in block_dict["transactions"]]
        return Block(
            block_dict["index"],
            block_dict["previous_hash"],
            transactions,
            block_dict["timestamp"]
        )

    def __repr__(self):
        return f"Block(index={self.index}, previous_hash={self.previous_hash}, hash={self.hash}, nonce={self.nonce})"

class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def __repr__(self):
        return f"Transaction({self.sender} -> {self.recipient} : {self.amount})"

class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.load_chain()  # Charger depuis JSON si dispo, sinon créer le bloc genesis

    def create_genesis_block(self):
        """
        Crée le premier bloc de la blockchain (bloc génésis).
        """
        return Block(0, "0", [])

    def is_valid_chain(self):
        """
        Vérifie l'intégrité de la blockchain.
        """
        for i, current in enumerate(self.chain[1:], start=1):
            previous = self.chain[i - 1]
            if current.previous_hash != previous.hash or current.hash != current.calculate_hash():
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

    def add_transaction(self, transaction):
        if not isinstance(transaction, Transaction):
            raise TypeError("Invalid transaction type")
        if transaction.amount <= 0:
            raise ValueError("Transaction amount must be positive")
        if not transaction.sender or not transaction.recipient:
            raise ValueError("Transaction must have a sender and a recipient")
        self.pending_transactions.append(transaction)

    def mine_new_block(self):
        if not self.pending_transactions:
            raise ValueError("No transactions to mine")
        last_block = self.chain[-1]
        new_block = Block(len(self.chain), last_block.hash, self.pending_transactions)
        new_block.mine_block(difficulty=2)
        self.chain.append(new_block)
        self.pending_transactions = []
        self.save_chain()