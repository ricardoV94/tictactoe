import itertools

import numpy as np

def loop_board():
    return enumerate(itertools.product(range(3), range(3)))

def plot_board_score(ax, scores, board):

    scores = np.asarray(scores)

    # Colors
    ax.imshow(
        scores.reshape(3, 3),
        vmin = -5,
        vmax = 5,
        cmap='coolwarm'
    )

    # Grid
    ax.set_xticks(np.arange(3)+.5)
    ax.set_yticks(np.arange(3)+.5)
    ax.grid(color="w", linestyle='-', linewidth=2)
    ax.set_xlim([-.5, 3])

    # Text labels
    for i, (row, col) in loop_board():
        if player := board.board[i]:
            piece = 'X' if player == 1 else 'O'
            ax.text(col, row, piece, ha='center', va='center', color='k', fontsize=16)
        else:
            ax.text(col, row, scores[i], ha="center", va="center", color="w", fontsize=12)

    clean_square(ax)


def clean_square(ax):
    ax.tick_params(which="minor", bottom=False, left=False)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(
        left=False,
        labelleft=False,
        bottom=False,
        labelbottom=False,
    )