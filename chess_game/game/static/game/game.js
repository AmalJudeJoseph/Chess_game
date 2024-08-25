const gameSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/game/'
);

gameSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log("Message received:", data);
    if (data.error) {
        alert(data.error);
    } else {
        updateGameBoard(data.board);
        updateCurrentTurn(data.current_turn);
        if (data.winner) {
            alert('Winner: ' + data.winner);
        }
    }
};

gameSocket.onopen = function(e) {
    console.log("WebSocket connection opened.");
};

gameSocket.onclose = function(e) {
    console.log("WebSocket connection closed. Code:", e.code, "Reason:", e.reason);
};

gameSocket.onerror = function(e) {
    console.error("WebSocket error:", e);
};

function updateGameBoard(board) {
    const boardElement = document.getElementById('game-board');
    boardElement.innerHTML = '';  // Clear the board
    for (let i = 0; i < board.length; i++) {
        let row = board[i];
        for (let j = 0; j < row.length; j++) {
            let cell = document.createElement('div');
            cell.className = 'board-cell';
            cell.innerHTML = row[j];
            boardElement.appendChild(cell);
        }
    }
}

function updateCurrentTurn(turn) {
    const turnElement = document.getElementById('current-turn');
    turnElement.innerText = 'Current Turn: ' + turn;
}

document.getElementById('start-game').onclick = function() {
    gameSocket.send(JSON.stringify({
        'command': 'start'
    }));
};
