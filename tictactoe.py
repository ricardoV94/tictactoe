from enum import Enum

X = 1
O = 2

class Board:
    def __init__(self, board=None):
        if board is None:
            board = [0] * 9
        self.board = tuple(board)

    def winner(self):
        board = self.board

        # Check diagonals
        if board[0] and board[0] == board[4] == board[8]:
            return board[0]
        if board[2] and board[2] == board[4] == board[6]:
            return board[2]

        # Check rows
        for row in range(3):
            if board[row*3] and board[row*3] == board[(row*3)+1] == board[(row*3)+2]:
                return board[row*3]
        
        # Check cols
        for col in range(3):
            if board[col] and board[col] == board[col+3] == board[col+6]:
                return board[col]

        return 0

    def game_over(self):
        board = self.board

        # Check if all squares are occupied
        if sum(bool(b) for b in board) == 9:
            return True

        # Check if there is a winner
        if self.winner():
            return True
        
        return False

    def generate_unique_legal_moves(self):
        # Generate legal moves from given board, ignoring symmetries

        unique_moves = []
        moves_hash = set()

        for move in self.generate_legal_moves():
            move_hash = hash(move)
            if move_hash in moves_hash:
                continue

            moves_hash.add(move_hash)
            unique_moves.append(move)

        return unique_moves

    def generate_legal_moves(self):
        # Generate legal moves from given board
    
        # Check gameover
        if self.game_over():
            return []

        side_to_move = self.side_to_move()

        legal_moves = []
        for square in range(9):
            if self.board[square] == 0:
                new_move = Board(self.board[:square] + (side_to_move,) + self.board[square+1:])
                legal_moves.append(new_move)
        return legal_moves

    def side_to_move(self):
        # Check side to move

        nX = sum(1 for n in self.board if n==X)
        nO = sum(1 for n in self.board if n==O)
        
        assert nX - nO in (0, 1)

        side_to_move = X if nX == nO else O
        return side_to_move

    def rotate(self, r=1):
        return Board(Board._rotate(self.board, r=r))

    @staticmethod
    def _rotate(board, r=1):
        # Rotate 90 degrees clockwise
        r -= 1
        # new_node = tuple(item for col in range(3) for item in reversed(node[col::3]))
        new_board = tuple(board[::3][::-1] + board[1::3][::-1] + board[2::3][::-1])
        if r:
            return Board._rotate(new_board, r)
        return new_board
 
    def flipH(self):
        # Flip across the middle row
        return Board(tuple(self.board[6:9] + self.board[3:6] + self.board[0:3]))
    
    def flipV(self):
        # Flip across the middle column
        return Board(tuple(self.board[:3][::-1] + self.board[3:6][::-1] + self.board[6:][::-1]))
    
    def flipD(self):
        # Flip across the diagonal
        return Board(Board._rotate(self.flipV().board))
    
    def flipA(self):
        # Flip across the antidiagonal
        return Board(Board._rotate(self.flipH().board))

    def symmetries(self):
        # Return all symmetries of node
        boards = [self]

        for r in range(1, 4):
            boards.append(self.rotate(r))

        for method in (self.flipH, self.flipV, self.flipD, self.flipA):
            boards.append(method())

        return boards

    def __eq__(self, other):
        if isinstance(other, Board):
            return self.board == other.board
        return NotImplemented

    def __hash__(self):
        symms = []
        for s in self.symmetries():
            value = 0
            for i, item in enumerate(s.board):
                value += item * 3 ** i
            symms.append(value)

        return min(symms)

    def __repr__(self):
        return f'Board({self.board})'

    def __str__(self):
        result = []
        for item in self.board:
            if item == X:
                result.append('X')
            elif item == O:
                result.append('O')
            else:
                result.append('.')
        result.insert(6, '\n')
        result.insert(3, '\n')
        return ' ' + ' '.join(result)



if __name__ == '__main__':

    def count_boards(board=None, boards=None, boards_hashes=None):
        if board is None:
            board = Board()
            boards = []
            boards_hashes = set()

            boards_hashes.add(hash(board))
            boards.append(board)
        
        for b in board.generate_unique_legal_moves():
            b_hash = hash(b)
            if b_hash in boards_hashes:
                continue

            boards_hashes.add(b_hash)
            boards.append(b)
            count_boards(b, boards, boards_hashes)
        
        return boards


    boards = count_boards()
    print('Equivalent boards:', len(boards))

    outcome = [b.winner() for b in boards]
    print('Games where X wins:', sum(out == 1 for out in outcome))
    print('Games where O wins:', sum(out == 2 for out in outcome))
    print('Games where neither wins:', sum(out == 0 for out in outcome))