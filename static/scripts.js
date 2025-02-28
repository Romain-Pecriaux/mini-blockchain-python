function showMessage(message) {
    document.getElementById('messageModalBody').innerText = message;
    $('#messageModal').modal('show');
}

// Fonction pour créer une nouvelle transaction
document.getElementById('transaction-form').onsubmit = async function(event) {
    event.preventDefault();
    const sender = document.getElementById('sender').value;
    const recipient = document.getElementById('recipient').value;
    const amount = document.getElementById('amount').value;
    try {
        const response = await fetch('/transaction', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ sender, recipient, amount })
        });
        if (response.status === 201) {
            showMessage('Transaction added');
            $('#transactionModal').modal('hide');
            updatePendingTransactions();
        } else {
            showMessage('Error adding transaction');
        }
    } catch (error) {
        showMessage('Error adding transaction');
    }
};

// Fonction pour miner un nouveau bloc
document.getElementById('mine-block').onclick = function() {
    fetch('/mine', { method: 'POST' })
        .then(response => {
            if (response.status === 201) {
                showMessage('Block mined');
                updateBlockchain();
                updatePendingTransactions();
            } else {
                showMessage('Error mining block');
            }
        });
};

// Fonction pour vérifier l'intégrité de la blockchain
document.getElementById('check-integrity').onclick = function() {
    fetch('/check_integrity')
        .then(response => response.json())
        .then(data => {
            showMessage(data.message);
        });
};

// Fonction pour mettre à jour les transactions en attente
function updatePendingTransactions() {
    fetch('/pending_transactions')
        .then(response => response.json())
        .then(data => {
            const pendingTransactionsDiv = document.getElementById('pending-transactions');
            pendingTransactionsDiv.innerHTML = '';
            data.forEach((transaction, index) => {
                const transactionDiv = document.createElement('div');
                transactionDiv.className = 'transaction';
                transactionDiv.innerHTML = `
                    <div class="transaction-info">
                        <div class="sender">Sender: ${transaction.sender}</div>
                        <div class="amount">Amount: ${transaction.amount}</div>
                        <div class="receiver">Receiver: ${transaction.recipient}</div>
                    </div>
                    <button class="btn btn-danger delete-btn" onclick="deleteTransaction(${index})">Delete</button>
                `;
                pendingTransactionsDiv.appendChild(transactionDiv);
            });
        });
}

// Fonction pour supprimer une transaction en attente
function deleteTransaction(index) {
    fetch(`/transaction/${index}`, { method: 'DELETE' })
        .then(response => {
            if (response.status === 200) {
                showMessage('Transaction deleted');
                updatePendingTransactions();
            } else {
                showMessage('Error deleting transaction');
            }
        });
}

// Fonction pour afficher la blockchain de manière visuelle
function displayBlockchain(blockchain) {
    const blockchainVisual = document.getElementById('blockchain-visual');
    blockchainVisual.innerHTML = '';
    blockchain.forEach(block => {
        const blockDiv = document.createElement('div');
        blockDiv.className = 'block';
        blockDiv.innerHTML = `
            <h3>Block ${block.index}</h3>
            <p>Previous Hash: ${block.previous_hash}</p>
            <p>Hash: ${block.hash}</p>
            <p>Nonce: ${block.nonce}</p>
            <p>Timestamp: ${new Date(block.timestamp * 1000).toLocaleString()}</p>
            <h4>Transactions:</h4>
            <ul>
                ${block.transactions.map(tx => `<li>${tx.sender} -> ${tx.recipient}: ${tx.amount}</li>`).join('')}
            </ul>
        `;
        blockchainVisual.appendChild(blockDiv);
    });
}

// Fonction pour mettre à jour la blockchain
function updateBlockchain() {
    fetch('/blockchain')
        .then(response => response.json())
        .then(data => {
            displayBlockchain(data);
        });
}

// Initialisation
updateBlockchain();
updatePendingTransactions();