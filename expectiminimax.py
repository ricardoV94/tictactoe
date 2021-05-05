import random
from statistics import mean

from tictactoe import Board, O, X


class ExpectiMiniMax:

    def __init__(self):
        self.board_evals = {
            X: {},
            O: {},
        }
        self.hits = 0

    def __getitem__(self, item):
        player, board = item
        return self.board_evals[player][hash(board)]

    def _search(self, board: Board, player: int):
        board_hash = hash(board)
        if board_hash in self.board_evals[player]:
            self.hits += 1
            bestmove, score, *_ = self.board_evals[player][board_hash].values()
            return score

        if board.game_over():
            winner = board.winner()

            if not winner:
                score = 0
            else:
                nmoves = sum(bool(sq) for sq in board.board)
                score = -10 + nmoves

            self.board_evals[player][board_hash] = {
                'bestmove': None, 'score': score,
                'moves': [], 'scores': [],
            }

            return score

        # Player turn
        moves = []
        scores = []
        if player == board.side_to_move():
            bestscore = -999
            bestmove = None
            for move in board.generate_unique_legal_moves():
                moves.append(move)
                score = -self._search(move, player)
                if score > bestscore:
                    bestscore = score
                    bestmove = move
                scores.append(score)

            self.board_evals[player][board_hash] = {
                'bestmove': bestmove, 'score': bestscore,
                'moves': moves, 'scores': scores,
            }
            return bestscore

        # Random opponent turn
        else:
            moves = []
            scores = []
            scores_hash = {}
            for move in board.generate_legal_moves():
                moves.append(move)
                move_hash = hash(move)

                # If equivalent move was already compute simply add it to the scores list
                if move_hash in scores_hash:
                    scores.append(scores_hash[move_hash])
                    continue

                score = -self._search(move, player)
                scores.append(score)
                scores_hash[move_hash] = score

            avg_score = mean(scores)
            self.board_evals[player][board_hash] = {
                'bestmove': None, 'score': avg_score,
                'moves': moves, 'scores': scores,
            }

            # Return average
            return avg_score

    def search(self, board: Board = None):
        if board is None:
            board = Board()
        player = board.side_to_move()
        return self._search(board, player)


if __name__ == '__main__':

    engine = ExpectiMiniMax()

    b = Board((0, 0, 0, 0, 0, 0, 0, 0, 0))

    print(engine.search(b))
    print(len(engine.board_evals))
    print(engine.hits)

    move, score, *_ = engine[(X, b)].values()
    while move:
        print('')
        print(f'{score=:.1f}')
        print(move)

        moves = move.generate_legal_moves()
        _, avg_score, moves, scores = engine[(X, move)].values()
        if not moves:
            break
        move = random.choice(moves)
        move_idx = moves.index(move)
        score = scores[move_idx]

        print('')
        print(f'{avg_score=:.1f}')
        print(f'{score=:.1f}')
        print(move)

        move, score, *_ = engine[(X, move)].values()

    print('')
    print('#'*20)
    b = Board()
    *_, moves, scores = engine[(X, b)].values()
    for move, score in zip(moves, scores):
        print('')
        print(f'{score=:.3f}')
        print(move)
