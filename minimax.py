from tictactoe import Board, O, X


class MiniMax:

    def __init__(self):
        self.board_evals = {}
        # self.search()
        self.hits = 0

    def __getitem__(self, board):
        return self.board_evals[hash(board)]

    def search(self, board: Board=None):
        if board is None:
            board = Board()

        board_hash = hash(board)
        if board_hash in self.board_evals:
            self.hits += 1
            bestmove, score = self.board_evals[board_hash].values()
            return score

        if board.game_over():
            winner = board.winner()

            if not winner:
                score = 0
            else:
                nmoves = sum(bool(sq) for sq in board.board)
                score = -10 + nmoves

            self.board_evals[board_hash] = {'bestmove': None, 'score': score}

            return score

        bestscore = -999
        bestmove = None
        for move in board.generate_unique_legal_moves():
            score = -self.search(move)
            if score > bestscore:
                bestscore = score
                bestmove = move

        self.board_evals[board_hash] = {'bestmove': bestmove, 'score': bestscore}
        return bestscore


if __name__ == '__main__':

    engine = MiniMax()

    b = Board((0, X, 0, 0, O, 0, X, 0, 0))

    print(engine.search(b))
    print(len(engine.board_evals))
    print(engine.hits)

    move, score = engine[b].values()
    while move:
        print('')
        print(f'{score=}')
        print(move)

        move, score = engine[move].values()

