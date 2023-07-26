#!/usr/bin/python3

import numpy as np
import nashpy as nash
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid

class InfectionAgent(Agent):
    def __init__(self, unique_id, model, payoffs):
        super().__init__(unique_id, model)
        self.infected = False
        self.payoffs = payoffs

    def move(self):
        x, y = self.pos
        neighbors = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )
        neighbor_payoffs = [self.payoffs[pos] for pos in neighbors]
        max_payoff_neighbors = [
            neighbors[i] for i, payoff in enumerate(neighbor_payoffs) if payoff == np.max(neighbor_payoffs)
        ]
        if max_payoff_neighbors:
            new_position = self.random.choice(max_payoff_neighbors)
            self.model.grid.move_agent(self, new_position)

        if self.infected:
            self.payoffs[self.pos] = -1

            
#infection function
    def infect(self):
        x, y = self.pos
        agents = self.model.grid.get_cell_list_contents([(x, y)])
        for agent in agents:
            if agent.unique_id != self.unique_id and not agent.infected:
                agent.infected = True
                self.payoffs[agent.pos] = -1  # Set negative payoff for the newly infected agent
                self.payoffs[self.pos] += 1  # Increase payoff for the infector

    def step(self):
        self.move()
        if self.infected:
            self.infect()
        print(f"agent {self.unique_id}; pos {self.pos}; infected {self.infected}; payoff[ {self.payoffs[self.pos]} ]")

class InfectionModel(Model):
    def __init__(self, N, width, height):
        self.num_agents = N
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(width, height, torus=True)
        self.payoffs = payoffs
        num_infected = 1
        self.num_infected = num_infected
        
        for i in range(self.num_agents):
            a = InfectionAgent(i, self, self.payoffs)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
            self.schedule.add(a)

        for _ in range(num_infected):
            agent = self.random.choice(self.schedule.agents)
            agent.infected = True
            self.payoffs[agent.pos] = -1

    def step(self):
        self.schedule.step()

# Create a 20x20 grid of payoffs
payoffs = np.zeros((100, 100))
payoffs[0:5, 0:5] = 1  #setting a region of high payoff
payoffs[15:20, 15:20] = -1#region with negative payoff

# Create an instance of the model with 100 agents and a 20x20 grid
model = InfectionModel(1000, 100, 100)

# Run the model for a certain number of steps
for i in range(10):
    model.step()
    print("__________________________________________________________")
