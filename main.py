from blockchain import Blockchain

# Initialisation
blockchain = Blockchain()

# Ajout de blocs
blockchain.add_block("Transaction 1")
blockchain.add_block("Transaction 2")

# Vérification de la blockchain
print("Blockchain valide ?", blockchain.is_valid_chain())

# Affichage des blocs
for block in blockchain.chain:
    print(block.to_dict())