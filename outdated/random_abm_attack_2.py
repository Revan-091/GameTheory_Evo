import math
import random
import matplotlib.pyplot as plt

# Agent class representing both teams A and B
class Agent:
    def __init__(self, team, position, health, attack_strength):
        self.team = team
        self.position = position
        self.health = health
        self.attack_strength = attack_strength
    
    def distance_to(self, target_agent):
        return math.sqrt((self.position[0] - target_agent.position[0])**2 + (self.position[1] - target_agent.position[1])**2)

    def attack(self, target_agent):
        target_agent.health -= self.attack_strength
        print(f"{self.team} agent attacked {target_agent.team} agent!")

# Simulation parameters
num_agents = 150  # Total number of agents 
max_steps = 100

# Create agents
agents = []
num_agents_a = num_agents // 2
num_agents_b = num_agents - num_agents_a

# Create agents for team A
for _ in range(num_agents_a):
    position = (random.uniform(0, 10), random.uniform(0, 10))
    health = 100#random.randint(50, 100)
    attack_strength = random.randint(10, 20)
    agents.append(Agent("A", position, health, attack_strength))

# Create agents for team B
for _ in range(num_agents_b):
    position = (random.uniform(0, 10), random.uniform(0, 10))
    health = 100#random.randint(50, 100)
    attack_strength = random.randint(10, 20)
    agents.append(Agent("B", position, health, attack_strength))

# Initialize figure and counter for visualization
fig, ax = plt.subplots()
counter = ax.text(8, 9.5, f"Agents B: {num_agents_b}", fontsize=12, ha='right')

# Simulation loop
for step in range(max_steps):
    # Iterate over all agents
    for agent in agents:
        if agent.team == "A":
            # Find the nearest enemy agent from team B
            nearest_enemy = min([a for a in agents if a.team == "B"], key=lambda a: agent.distance_to(a))
            if agent.distance_to(nearest_enemy) < 1.0:
                # Attack the nearest enemy agent
                agent.attack(nearest_enemy)
                if nearest_enemy.health <= 0:
                    agents.remove(nearest_enemy)
                    print(f"{nearest_enemy.team} agent died!")
            else:
                # Move towards the nearest enemy agent
                dx = nearest_enemy.position[0] - agent.position[0]
                dy = nearest_enemy.position[1] - agent.position[1]
                dx /= agent.distance_to(nearest_enemy)
                dy /= agent.distance_to(nearest_enemy)
                agent.position = (agent.position[0] + dx, agent.position[1] + dy)
        
        elif agent.team == "B":
            # Find the nearest enemy agent from team A
            nearest_enemy = min([a for a in agents if a.team == "A"], key=lambda a: agent.distance_to(a))
            if agent.distance_to(nearest_enemy) < 1.0:
                # Attack the nearest enemy agent
                agent.attack(nearest_enemy)
                if nearest_enemy.health <= 0:
                    agents.remove(nearest_enemy)
                    print(f"{nearest_enemy.team} agent died!")
            else:
                # Move towards the nearest enemy agent
                dx = nearest_enemy.position[0] - agent.position[0]
                dy = nearest_enemy.position[1] - agent.position[1]
                dx /= agent.distance_to(nearest_enemy)
                dy /= agent.distance_to(nearest_enemy)
                agent.position = (agent.position[0] + dx, agent.position[1] + dy)

    # Clear the previous frame
    ax.clear()

    # Plot agents
    for agent in agents:
        color = 'red' if agent.team == 'A' else 'blue'
        marker = 'o' if agent.team == 'A' else 'x'
        ax.scatter(agent.position[0], agent.position[1], c=color, marker=marker)

    # Set plot limits
    ax.set_xlim([0, 10])
    ax.set_ylim([0, 10])

    # Add labels and title
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title(f'Step {step + 1}')

    # Update and display counter
    remaining_agents_b = len([agent for agent in agents if agent.team == 'B'])
    counter.set_text(f"Agents B: {remaining_agents_b}")

    # Print agents' health
    print(f"Step {step + 1}:")
    for i, agent in enumerate(agents):
        print(f"Agent {i + 1} - Team: {agent.team}, Health: {agent.health}")
    
    # Pause to visualize each step
    plt.pause(0.1)

# Check winning team and display message
remaining_agents_a = len([agent for agent in agents if agent.team == 'A'])
remaining_agents_b = len([agent for agent in agents if agent.team == 'B'])
if remaining_agents_a == 0:
    print("Team B won!")
elif remaining_agents_b == 0:
    print("Team A won!")

# Display the final plot
plt.show()
