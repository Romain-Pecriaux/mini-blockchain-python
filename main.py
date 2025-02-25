from blockchain import Blockchain
from blockchain import Transaction

# Initialisation
blockchain = Blockchain()

# Ajout de blocs
blockchain.add_transaction(Transaction("Alice", "Bob", 10))
blockchain.add_transaction(Transaction("Bob", "Charlie", 5))

# Minage d'un nouveau bloc
blockchain.mine_new_block()

# Ajout d'une autre transaction et minage d'un autre bloc
blockchain.add_transaction(Transaction("Charlie", "Alice", 3))
blockchain.mine_new_block()

# Vérification de la blockchain
print("Blockchain valide ?", blockchain.is_valid_chain())

# Affichage des blocs
for block in blockchain.chain:
    print(block.to_dict())