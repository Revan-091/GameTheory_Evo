import math
import random
import matplotlib.pyplot as plt
import argparse
import numpy as np
import sys

# local import of the game theory actions (we precompute the actions for both teams)
from stochastic_gt import generate_agent_actions

# Agent class representing both teams A and B
class Agent:
    def __init__(self, team, agent_type, position, health, attack_range, attack_strength):
        self.team = team
        self.agent_type = agent_type
        self.position = position
        self.health = health
        self.attack_range = attack_range
        self.attack_strength = attack_strength
        self.last_action = "attack"  # Store the last action taken by the agent
    
    def distance_to(self, target_agent):
        return math.sqrt((self.position[0] - target_agent.position[0])**2 + (self.position[1] - target_agent.position[1])**2)

    def attack(self, target_agent):
        target_agent.health -= self.attack_strength
        print(f"{self.team} {self.agent_type} attacked {target_agent.team} {target_agent.agent_type}!")

    def min_health_of_opponents(self, other_agents):
        return min(agent.health for agent in other_agents if agent.team != self.team)

    def get_agents_in_range(self, agents, range_distance):
        return [agent for agent in agents if agent != self and self.distance_to(agent) <= 40]#range_distance]

    def count_friends_and_enemies(self, agents_in_range):
        friends = [agent for agent in agents_in_range if agent.team == self.team]
        enemies = [agent for agent in agents_in_range if agent.team != self.team]
        return len(friends), len(enemies)

    def retreat_to_common_point(self, agents, common_point):
        common_point = (50, 50)
        dx = common_point[0] - self.position[0]
        dy = common_point[1] - self.position[1]
        dx /= self.distance_to(common_point)
        dy /= self.distance_to(common_point)
        self.position = (self.position[0] - dx, self.position[1] - dy)

def create_formations(agents):
    soldiers_a = [agent for agent in agents if agent.team == 'A' and agent.agent_type == 'Soldier']
    cavalry_a = [agent for agent in agents if agent.team == 'A' and agent.agent_type == 'Cavalry']

    soldiers_b = [agent for agent in agents if agent.team == 'B' and agent.agent_type == 'Soldier']
    cavalry_b = [agent for agent in agents if agent.team == 'B' and agent.agent_type == 'Cavalry']

    formation_a = soldiers_a + cavalry_a
    formation_b = soldiers_b + cavalry_b 

    return formation_a, formation_b


# Function to parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description='Simulate a battle between two teams with soldiers, and cavalry.')
    parser.add_argument('--num_soldiers', type=int, default=600, help='Number of soldiers per team')
    parser.add_argument('--num_cavalry', type=int, default=400, help='Number of cavalry per team')
    return parser.parse_args()

# Function to get the best response strategy for a player
def get_best_response(player, opponent_strategy):
    print("This works")
    best_response_index = np.argmax(payoff_matrix[(player, opponent_strategy)][:, players.index(player)])
    return strategies[player][best_response_index]


def main():
    # Simulation parameters
    args = parse_arguments()
    num_soldiers_a = args.num_soldiers // 2
    num_cavalry_a = args.num_cavalry // 2
    num_agents_a = num_soldiers_a  + num_cavalry_a
    num_agents_b = args.num_soldiers - num_soldiers_a +  args.num_cavalry - num_cavalry_a
    num_agents = num_agents_a + num_agents_b
    max_steps = 1000

    deaths_A = {}
    deaths_B = {}
    for step in range(max_steps):
        deaths_A[step + 1] = 0 
        deaths_B[step + 1] = 0

    agent_a_actions, agent_b_actions = generate_agent_actions()

    # Create agents
    agents = []
    num_agents_a = int(num_agents * 0.44)  # Assuming 56% are from Team B
    num_cavalry_a = num_agents_a // 6  # Assuming 1/6 of Team A agents are Cavalry
    num_soldiers_a = num_agents_a - num_cavalry_a
    num_agents_b = num_agents - num_agents_a
    num_cavalry_b = num_agents_b // 6  # Assuming 1/6 of Team B agents are Cavalry
    num_soldiers_b = num_agents_b - num_cavalry_b

    initial_agents_a = num_agents_a
    initial_agents_b = num_agents_b

    
    # Create agents for team A
    for _ in range(num_soldiers_a):
        position1 = (random.uniform(2, 10), random.uniform(85, 145))
        position2 = (random.uniform(45, 70), random.uniform(155, 170))
        position3 = (random.uniform(90, 145), random.uniform(155, 165))
        position4 = (random.uniform(155, 190), random.uniform(145, 160))
        pos_list = [position1, position2, position3, position4]
        for i in range(num_soldiers_a):
            position = random.choice(pos_list)
        health = 100
        attack_range = random.uniform(1, 25)
        attack_strength = random.uniform(20, 30)
        agents.append(Agent("A", "Soldier", position, health, attack_range, attack_strength))

    for _ in range(num_cavalry_a):
        position1 = (random.uniform(7, 9), random.uniform(105, 160))
        position2 = (random.uniform(45, 60), random.uniform(165, 168))
        position3 = (random.uniform(90, 145), random.uniform(155, 159))
        position4 = (random.uniform(155, 190), random.uniform(145, 150))
        pos_list = [position1, position2, position3, position4]
        for i in range(num_soldiers_a):
            position = random.choice(pos_list)
        health = 150
        attack_range = random.uniform(6, 10)  # Cavalry has a slightly longer attack range than Soldier
        attack_strength = random.uniform(45, 60)  # Cavalry's attack strength
        agents.append(Agent("A", "Cavalry", position, health, attack_range, attack_strength))

    # Create agents for team B
    for _ in range(num_soldiers_b):
        position1 = (random.uniform(30, 45), random.uniform(95, 130))
        position2 = (random.uniform(50, 70), random.uniform(125, 130))
        position3 = (random.uniform(90, 145), random.uniform(120, 138))
        position4 = (random.uniform(155, 190), random.uniform(130, 135))
        pos_list = [position1, position2, position3, position4]
        for i in range(num_soldiers_a):
            position = random.choice(pos_list)
        health = 100
        attack_range = random.uniform(1, 25) 
        attack_strength = random.randint(20, 30)  
        agents.append(Agent("B", "Soldier", position, health, attack_range, attack_strength))

    for _ in range(num_cavalry_b):
        position1 = (random.uniform(25, 35), random.uniform(95, 130))
        position2 = (random.uniform(50, 70), random.uniform(128, 130))
        position3 = (random.uniform(90, 145), random.uniform(130, 138))
        position4 = (random.uniform(155, 190), random.uniform(133, 135))
        pos_list = [position1, position2, position3, position4]
        for i in range(num_soldiers_a):
            position = random.choice(pos_list)
        health = 150
        attack_range = random.uniform(2, 8)  # Cavalry has a slightly longer attack range than Soldier
        attack_strength = random.uniform(45, 60)  # Cavalry's attack strength
        agents.append(Agent("B", "Cavalry", position, health, attack_range, attack_strength))

    # Initialize figure and counter for visualization
    fig, ax = plt.subplots()
    counter = ax.text(8, 9.5, f"Agents B: {num_agents_b}", fontsize=12, ha='right')

    # Simulation loop
    for step in range(max_steps):
        # Update step_counter at the beginning of each iteration
        formation_a, formation_b = create_formations(agents)
        
        remaining_agents_a = len([agent for agent in agents if agent.team == 'A'])
        remaining_agents_b = len([agent for agent in agents if agent.team == 'B'])
        
        if remaining_agents_a < num_agents_a * 0.3:
            print("____________")
            print("Team B won!")
            print("____________")
            sys.exit()
        elif remaining_agents_b < num_agents_b * 0.3:
            print("____________")
            print("Team A won!")
            print("____________")
            sys.exit()
        
        active_agents = len(agents)
        for agent in agents:
            # Find the nearest enemy agent from the opposite team
            nearest_enemy = min([a for a in agents if a.team != agent.team], key=lambda a: agent.distance_to(a))
            nearest_friend = min([a for a in agents if a.team == agent.team], key=lambda a: agent.distance_to(a))
            opponent_strategy = nearest_enemy.last_action
            if agent.team == "A":
                chosen_action = agent_a_actions[step]
            else:
                chosen_action = agent_b_actions[step]
            # Get agents in range of the current agent
            agents_in_range = agent.get_agents_in_range(agents, agent.attack_range)
            if agent.agent_type == 'Soldier' or agent.agent_type == 'Cavalry':
                if chosen_action == 'attack':
                    # Move towards the nearest enemy agent
                    dx = nearest_enemy.position[0] - agent.position[0]
                    dy = nearest_enemy.position[1] - agent.position[1]
                    dx /= agent.distance_to(nearest_enemy)
                    dy /= agent.distance_to(nearest_enemy)
                    agent.position = (agent.position[0] + dx, agent.position[1] + dy)
                else:
                    retreat_point = (100, 100)
                    # Move towards the fixed retreat point (100, 100) if not attacking
                    dx = retreat_point[0] - agent.position[0]
                    dy = retreat_point[1] - agent.position[1]
                    norm = math.sqrt(dx**2 + dy**2)  # Calculate the norm of the vector
                    if norm != 0:
                        dx /= norm  # Normalize the x-component
                        dy /= norm  # Normalize the y-component
                    agent.position = (agent.position[0] + dx, agent.position[1] + dy)


                # Attack if an enemy is within the agent's attack range
                if agent.distance_to(nearest_enemy) <= agent.attack_range:
                    agent.attack(nearest_enemy)
                    if nearest_enemy.health <= 0:
                        agents.remove(nearest_enemy)
                        print(f"{nearest_enemy.team} {nearest_enemy.agent_type} died!")
                        

        # Clear the previous frame
        ax.clear()

        # Plot agents
        for agent in agents:
            if agent.team == 'A':
                color = 'salmon' if agent.agent_type == 'Soldier' else 'indianred'  # Soldiers: salmon, Cavalry: indianred
                marker = 'X' if agent.agent_type == 'Soldier' else 's'  # Soldiers: X, Cavalry: s
            if agent.team == "B":
                color = 'lightblue' if agent.agent_type == 'Soldier' else 'royalblue'  # Soldiers: lightblue, Cavalry: royalblue
                marker = 'o' if agent.agent_type == 'Soldier' else 'D'  # Soldiers: o, Cavalry: D
            ax.scatter(agent.position[0], agent.position[1], c=color, marker=marker)

        # Set plot limits
        ax.set_xlim([0, 200])
        ax.set_ylim([0, 200])

        # Add labels and title
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title(f'Step {step + 1}')

        # Update and display counter
        remaining_agents_b = len([agent for agent in agents if agent.team == 'B'])
        counter.set_text(f"Agents B: {remaining_agents_b}")

        # Pause to visualize each step
        plt.pause(0.1)

    # Display the final plot
    plt.show()

if __name__ == "__main__":
    main()

