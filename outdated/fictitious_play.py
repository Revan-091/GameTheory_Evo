import nashpy as nash
import numpy as np

A = np.array([[0, -1, -1], [1, 0, -1], [1, 1, 0]])
B = np.array([[0, 1, 1], [-1, 0, 1], [-1, -1, 0]])
game = nash.Game(A, B)
print(game)

game.replicator.dynamics()

"""np.random.seed(1)
iterations = 1000
play_counts = game.fictitious_play(iterations=iterations)
for row_play_counts, col_play_counts in play_counts:
    print(row_play_counts, col_play_counts)
"""
