from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid


class Agent(Agent):
    def __init__(self, unique_id, model, x, y, group):
        super().__init__(unique_id, model)
        self.x = x
        self.y = y
        self.group = group
        self.health = 100

    def move(self):
        x, y = self.pos
        neighbors = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )
        enemy_agents = [agent for agent in self.model.schedule.agents if agent.group != self.group]
        if enemy_agents:
            distances = [self.model.grid.get_distance(self.pos, agent.pos) for agent in enemy_agents]
            closest_enemy = enemy_agents[distances.index(min(distances))]
            dx = 0 if x == closest_enemy.x else 1 if x < closest_enemy.x else -1
            dy = 0 if y == closest_enemy.y else 1 if y < closest_enemy.y else -1
            new_position = (x + dx, y + dy)
            self.model.grid.move_agent(self, new_position)

    def attack(self):
        x, y = self.pos
        targets = self.model.grid.get_cell_list_contents([(x, y)])
        for target in targets:
            if target.group != self.group:
                target.health -= 10
                if target.health <= 0:
                    self.model.teams[target.group] -= 1

    def step(self):
        self.move()
        self.attack()

class BattleModel(Model):
    def __init__(self, n, m, box_size, center_x_A, center_y_A, center_x_B, center_y_B):
        self.num_agents = 0
        self.grid = MultiGrid(n, m, torus=True)
        self.schedule = RandomActivation(self)
        self.population = [[0 for _ in range(m)] for _ in range(n)]
        self.teams = {"A": 0, "B": 0}
        
        agents_A = self.create_agents("A", center_x_A, center_y_A, box_size)
        agents_B = self.create_agents("B", center_x_B, center_y_B, box_size)
        
        for agent in agents_A:
            self.population[agent.x][agent.y] = 1
            self.teams["A"] += 1
        for agent in agents_B:
            self.population[agent.x][agent.y] = 2
            self.teams["B"] += 1
        

    def create_agents(self, group, center_x, center_y, box_size):
        agents = []
        start_x = center_x - box_size // 2
        start_y = center_y - box_size // 2
        
        for i in range(box_size):
            for j in range(box_size):
                x = start_x + i 
                y = start_y + j 
                agent = Agent(self.num_agents, self, x, y, group)
                agents.append(agent)
                self.grid.place_agent(agent, (x, y))
                self.schedule.add(agent)
                self.num_agents += 1

        return agents
    
    def step(self):
        self.schedule.step()
        
class PopulationVisualization:
    def __init__(self, model):
        self.model = model

    def update_population(self):
        self.model.population = [[0 for _ in range(self.model.grid.width)] for _ in range(self.model.grid.height)]
        for agent in self.model.schedule.agents:
            self.model.population[agent.x][agent.y] = 1 if agent.group == "A" else 2

    def plot_population(self):
        plt.figure(figsize=(12, 12))
        plt.title("Agent Population (Blue = 1000, Red = 1000)", fontsize=24)
        plt.xlabel("X Coordinates", fontsize=20)
        plt.ylabel("Y Coordinates", fontsize=20)
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        plt.imshow(X=self.model.population, cmap=self.model.colormap)

        # Add grid legend
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', label='Empty', markerfacecolor='lightgreen', markersize=10),
            plt.Line2D([0], [0], marker='o', color='w', label='Group A', markerfacecolor='red', markersize=10),
            plt.Line2D([0], [0], marker='o', color='w', label='Group B', markerfacecolor='blue', markersize=10)
        ]
        plt.legend(handles=legend_elements, loc='upper right')

        plt.show()

# Create an instance of the model
n = 100
m = 100
box_size = 25
center_x_A = n // 3
center_y_A = m // 3
center_x_B = 2 * (n // 3)
center_y_B = 2 * (m // 3)
model = BattleModel(n, m, box_size, center_x_A, center_y_A, center_x_B, center_y_B)

# Create an instance of the visualization class
visualization = PopulationVisualization(model)

# Run the model for a certain number of steps
for i in range(10):
    model.step()
    visualization.update_population()
    visualization.plot_population()
