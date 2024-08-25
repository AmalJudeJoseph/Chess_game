import json
from channels.generic.websocket import WebsocketConsumer
from .models import Game

class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.game = Game.objects.create()
        self.game.initialize_board()
        self.send_board_state()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # Handle received data, e.g., move processing
        self.send(text_data=json.dumps({
            'message': 'Hello from the server!'
        }))
        data = json.loads(text_data)
        move = data.get('move')
        player = data.get('player')

        if move and player:
            success = self.game.move(player, move['character'], move['direction'])
            if success:
                self.send_board_state()
            else:
                self.send_invalid_move()

    def send_board_state(self):
        self.send(text_data=json.dumps({
            'board': self.game.board,
            'current_turn': self.game.current_turn,
            'winner': self.game.winner
        }))

    def send_invalid_move(self):
        self.send(text_data=json.dumps({
            'error': 'Invalid move'
        }))

    def disconnect(self, close_code):
        pass
