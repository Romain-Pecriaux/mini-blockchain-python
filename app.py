from flask import Flask, jsonify, request, render_template, abort
from blockchain import Blockchain, Transaction

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/')
def index():
    """
    Route pour la page d'accueil.
    """
    return render_template('index.html')

@app.route('/blockchain', methods=['GET'])
def get_blockchain():
    """
    Route pour obtenir la blockchain complète.
    """
    chain_data = [block.to_dict() for block in blockchain.chain]
    return jsonify(chain_data), 200

@app.route('/transaction', methods=['POST'])
def create_transaction():
    """
    Route pour créer une nouvelle transaction.
    """
    data = request.get_json()
    required_fields = ['sender', 'recipient', 'amount']
    if not all(field in data for field in required_fields):
        abort(400, description='Missing fields')
    try:
        amount = float(data['amount'])
        if amount <= 0:
            abort(400, description='Invalid amount')
        transaction = Transaction(data['sender'], data['recipient'], amount)
        blockchain.add_transaction(transaction)
        return jsonify({'message': 'Transaction added'}), 201
    except ValueError:
        abort(400, description='Invalid amount')
    except TypeError as e:
        abort(400, description=str(e))

@app.route('/transaction/<int:index>', methods=['DELETE'])
def delete_transaction(index):
    """
    Route pour supprimer une transaction en attente.
    """
    try:
        blockchain.pending_transactions.pop(index)
        return jsonify({'message': 'Transaction deleted'}), 200
    except IndexError:
        return jsonify({'error': 'Transaction not found'}), 404

@app.route('/pending_transactions', methods=['GET'])
def get_pending_transactions():
    """
    Route pour obtenir les transactions en attente.
    """
    transactions = [t.__dict__ for t in blockchain.pending_transactions]
    return jsonify(transactions), 200

@app.route('/mine', methods=['POST'])
def mine_block():
    """
    Route pour miner un nouveau bloc.
    """
    try:
        blockchain.mine_new_block()
        return 'Block mined', 201
    except ValueError as e:
        return str(e), 400

@app.route('/check_integrity', methods=['GET'])
def check_integrity():
    """
    Route pour vérifier l'intégrité de la blockchain.
    """
    is_valid = blockchain.is_valid_chain()
    message = "Blockchain is valid" if is_valid else "Blockchain is not valid"
    return jsonify({'message': message}), 200

if __name__ == '__main__':
    app.run(debug=True)