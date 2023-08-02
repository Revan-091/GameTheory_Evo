import nashpy as nash
import numpy as np

agents = [agent for agent in range(500)]

A = np.array([[3, -2], [-1, 2]])
game = nash.Game(A)

np.random.seed(0)
iterations = 500
play_counts_and_distributions = game.stochastic_fictitious_play(iterations=iterations)

# List to store the output
output_list = []

# Lists to store actions for row and column distributions
row_actions_list = []
column_actions_list = []

for _, distributions in play_counts_and_distributions:
    row_distributions, column_distributions = distributions
    output_list.append((row_distributions, column_distributions))
    # Sample actions from distributions and add them to the respective lists
    row_action = "attack"
    column_action = np.random.choice(["attack", "defend"], p=column_distributions)
    row_actions_list.append(row_action)
    column_actions_list.append(column_action)

# Print the row and column distributions and actions for each iteration
for i, (row_distributions, column_distributions) in enumerate(output_list):
    print(f"Iteration {i + 1}:")
    print("Row Action:", row_actions_list[i])
    print("Column Action:", column_actions_list[i])
    print("---")
