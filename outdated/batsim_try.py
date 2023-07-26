import matplotlib.pyplot as plt
from matplotlib import colors

class Agent:
    def __init__(self, x, y, group):
        self.x = x
        self.y = y
        self.group = group

def create_agents(size, group, field, n, m, center_x, center_y, box_size):
    agents = []
    start_x = center_x - box_size // 2
    start_y = center_y - box_size // 2
    
    for i in range(box_size):
        for j in range(box_size):
            x = start_x + i 
            y = start_y + j 
            agent = Agent(x, y, group)
            agents.append(agent)
            field[x][y] = agent

    return agents

n = 100
m = 100
battlefield = [[None for _ in range(m)] for _ in range(n)]

box_size = 25  # Size of each box formation
center_x_A = n // 3
center_y_A = m // 3
center_x_B = 2 * (n // 3)
center_y_B = 2 * (m // 3)

agents_A = create_agents(1000, "A", battlefield, n, m, center_x_A, center_y_A, box_size)
agents_B = create_agents(1000, "B", battlefield, n, m, center_x_B, center_y_B, box_size)

population = [[0 for _ in range(m)] for _ in range(n)]
for agent in agents_A:
    population[agent.x][agent.y] = 1
for agent in agents_B:
    population[agent.x][agent.y] = 2

# Move the formations
center_x_A += 0
center_y_A -= 0
center_x_B -= 5
center_y_B += 10

battlefield = [[None for _ in range(m)] for _ in range(n)]
agents_A = create_agents(1000, "A", battlefield, n, m, center_x_A, center_y_A, box_size)
agents_B = create_agents(1000, "B", battlefield, n, m, center_x_B, center_y_B, box_size)

population = [[0 for _ in range(m)] for _ in range(n)]
for agent in agents_A:
    population[agent.x][agent.y] = 1
for agent in agents_B:
    population[agent.x][agent.y] = 2

colormap = colors.ListedColormap(["lightgreen", "red", "blue"])

plt.figure(figsize=(12, 12))
plt.title("Agent Population (Blue = 1000, Red = 1000)", fontsize=24)
plt.xlabel("X Coordinates", fontsize=20)
plt.ylabel("Y Coordinates", fontsize=20)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.imshow(X=population, cmap=colormap)

# Add grid legend
legend_elements = [
    plt.Line2D([0], [0], marker='o', color='w', label='Empty', markerfacecolor='lightgreen', markersize=10),
    plt.Line2D([0], [0], marker='o', color='w', label='Group A', markerfacecolor='red', markersize=10),
    plt.Line2D([0], [0], marker='o', color='w', label='Group B', markerfacecolor='blue', markersize=10)
]
plt.legend(handles=legend_elements, loc='upper right')

plt.show()
