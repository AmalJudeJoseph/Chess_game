from django.db import models

class Game(models.Model):
    board = models.JSONField(default=list)
    current_turn = models.CharField(max_length=1, default='A')
    winner = models.CharField(max_length=1, blank=True, null=True)

    def initialize_board(self):
        # Initialize a 5x5 grid with characters placed at starting positions
        self.board = [['' for _ in range(5)] for _ in range(5)]
        self.current_turn = 'A'
        self.save()

    def move(self, player, character, direction):
        # Implement the game logic for moving characters
        pass

    def check_winner(self):
        # Implement logic to check if there is a winner
        pass

    def move(self, player, character, direction):
        # Locate the character on the board
        x, y = self.find_character_position(player, character)
        new_x, new_y = self.calculate_new_position(x, y, character, direction)
        
        # Check for invalid moves
        if not self.is_valid_move(new_x, new_y, character):
            return False

        # Handle the move and update the board
        if self.board[new_x][new_y]:  # If the new position is occupied by opponent
            self.capture_opponent(new_x, new_y)

        self.board[x][y] = ''  # Clear the old position
        self.board[new_x][new_y] = f'{player}-{character}'  # Move character to new position

        # Switch turn
        self.current_turn = 'B' if player == 'A' else 'A'
        self.save()

        # Check for a winner
        self.check_winner()
        return True

    def find_character_position(self, player, character):
        for i in range(5):
            for j in range(5):
                if self.board[i][j] == f'{player}-{character}':
                    return i, j
        return None, None

    def calculate_new_position(self, x, y, character, direction):
        # Implement logic based on character type and direction
        if character.startswith('P'):  # Pawn
            return self.calculate_pawn_move(x, y, direction)
        elif character.startswith('H1'):  # Hero1
            return self.calculate_hero1_move(x, y, direction)
        elif character.startswith('H2'):  # Hero2
            return self.calculate_hero2_move(x, y, direction)

    def calculate_pawn_move(self, x, y, direction):
        moves = {'L': (0, -1), 'R': (0, 1), 'F': (-1, 0), 'B': (1, 0)}
        dx, dy = moves[direction]
        return x + dx, y + dy

    def calculate_hero1_move(self, x, y, direction):
        moves = {'L': (0, -2), 'R': (0, 2), 'F': (-2, 0), 'B': (2, 0)}
        dx, dy = moves[direction]
        return x + dx, y + dy

    def calculate_hero2_move(self, x, y, direction):
        moves = {'FL': (-2, -2), 'FR': (-2, 2), 'BL': (2, -2), 'BR': (2, 2)}
        dx, dy = moves[direction]
        return x + dx, y + dy

    def is_valid_move(self, x, y, character):
        # Check if the move is within bounds and the target position is valid
        return 0 <= x < 5 and 0 <= y < 5

    def capture_opponent(self, x, y):
        # Implement logic to capture opponent's character
        self.board[x][y] = ''

    def check_winner(self):
        # Implement logic to check if one player has eliminated all opponent characters
        pass
