import math
import random
import matplotlib.pyplot as plt
import argparse
import numpy as np
#Lo que me queda hacer:  -Elegir una batalla y estudiar los movimientos, aplicar game theory (iaia-o)


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
        dx = common_point[0] - self.position[0]
        dy = common_point[1] - self.position[1]
        dx /= self.distance_to(common_point)
        dy /= self.distance_to(common_point)
        self.position = (self.position[0] - dx, self.position[1] - dy)


def create_formations(agents):
    soldiers_a = [agent for agent in agents if agent.team == 'A' and agent.agent_type == 'Soldier']
    cavalry_a = [agent for agent in agents if agent.team == 'A' and agent.agent_type == 'Cavalry']
    archers_a = [agent for agent in agents if agent.team == 'A' and agent.agent_type == 'Archer']

    soldiers_b = [agent for agent in agents if agent.team == 'B' and agent.agent_type == 'Soldier']
    cavalry_b = [agent for agent in agents if agent.team == 'B' and agent.agent_type == 'Cavalry']
    archers_b = [agent for agent in agents if agent.team == 'B' and agent.agent_type == 'Archer']

    formation_a = soldiers_a + cavalry_a + archers_a
    formation_b = soldiers_b + cavalry_b + archers_b

    return formation_a, formation_b


# Function to parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description='Simulate a battle between two teams with soldiers, archers, and cavalry.')
    parser.add_argument('--num_soldiers', type=int, default=250, help='Number of soldiers per team')
    parser.add_argument('--num_archers', type=int, default=125, help='Number of archers per team')
    parser.add_argument('--num_cavalry', type=int, default=125, help='Number of cavalry per team')
    return parser.parse_args()

#Game Theory implementation
# Define the players and their strategies
players = ["A", "B"]
strategies = {
    "A": ["Attack", "Defend"],
    "B": ["Attack", "Defend"]
}

# Define the payoff matrix (using random values for demonstration)
payoff_matrix = {
    ("Attack", "Attack"): np.array([[100, 50], [50, 100]]),
    ("Attack", "Defend"): np.array([[70, 20], [10, 40]]),
    ("Defend", "Attack"): np.array([[40, 10], [20, 70]]),
    ("Defend", "Defend"): np.array([[50, 50], [50, 50]])
}

# Function to get the best response strategy for a player
def get_best_response(player, opponent_strategy):
    print("This works")
    best_response_index = np.argmax(payoff_matrix[(player, opponent_strategy)][:, players.index(player)])
    return strategies[player][best_response_index]


# Win-Stay, Lose-Shift strategy implementation
def win_stay_lose_shift_archer(agent, nearest_enemy):
    if agent.agent_type == 'Archer':
        if nearest_enemy.health > 0:
            # If the enemy is within the Archer's attack range, attack
            if agent.distance_to(nearest_enemy) <= agent.attack_range:
                agent.attack(nearest_enemy)
                if nearest_enemy.health <= 0:
                    agents.remove(nearest_enemy)
                    print(f"{nearest_enemy.team} {nearest_enemy.agent_type} died!")
                    if agent.team == "A":
                        deaths_B[step + 1] += 1  # Increment deaths counter for Team B
                        with open('deaths_team_b.csv', 'a') as file:
                            file.write(f"{step + 1},{deaths_B[step + 1]}\n")
                    elif agent.team == "B":
                        deaths_A[step + 1] += 1  # Increment deaths counter for Team A
                        with open('deaths_team_a.csv', 'a') as file:
                            file.write(f"{step + 1},{deaths_A[step + 1]}\n")
            else:
                # Move away from the nearest enemy agent to maintain formation
                dx = agent.position[0] - nearest_enemy.position[0]
                dy = agent.position[1] - nearest_enemy.position[1]
                dx /= agent.distance_to(nearest_enemy)
                dy /= agent.distance_to(nearest_enemy)
                agent.position = (agent.position[0] - dx, agent.position[1] - dy)

    # Store the current action for the next step
    agent.last_action = "attack" if nearest_enemy.health > 0 else "move"



def main():
    # Simulation parameters
    args = parse_arguments()
    num_soldiers_a = args.num_soldiers // 2
    num_archers_a = args.num_archers // 2
    num_cavalry_a = args.num_cavalry // 2
    num_agents_a = num_soldiers_a + num_archers_a + num_cavalry_a
    num_agents_b = args.num_soldiers - num_soldiers_a + args.num_archers - num_archers_a + args.num_cavalry - num_cavalry_a
    num_agents = num_agents_a + num_agents_b
    max_steps = 1000

    deaths_A = {}
    deaths_B = {}
    for step in range(max_steps):
        deaths_A[step + 1] = 0 
        deaths_B[step + 1] = 0

    # Create agents
    agents = []
    num_agents_a = num_agents // 2
    num_soldiers_a = num_agents_a // 2
    num_archers_a = num_agents_a // 4  # Assuming 1/4 of Team A agents are Archers
    num_cavalry_a = num_agents_a // 4  # Assuming 1/4 of Team A agents are Cavalry
    num_agents_b = num_agents - num_agents_a
    num_soldiers_b = num_agents_b // 2
    num_archers_b = num_agents_b // 4  # Assuming 1/4 of Team B agents are Archers
    num_cavalry_b = num_agents_b // 4  # Assuming 1/4 of Team B agents are Cavalry

    # Create agents for team A
    for _ in range(num_archers_a):
        position = (random.uniform(0, 53), random.uniform(170, 200))
        health = 80
        attack_range = random.uniform(30, 50)  # Archers have a longer attack range
        attack_strength = random.randint(15, 40)  # Archers hit less hard
        agents.append(Agent("A", "Archer", position, health, attack_range, attack_strength))

    for _ in range(num_soldiers_a):
        position = (random.uniform(0, 200), random.uniform(140, 170))
        health = 100
        attack_range = random.uniform(1, 5)
        attack_strength = random.uniform(20, 30)
        agents.append(Agent("A", "Soldier", position, health, attack_range, attack_strength))

    for _ in range(num_cavalry_a):
        position = (random.uniform(0, 200), random.uniform(120, 140))  # Adjust position as desired
        health = 150
        attack_range = random.uniform(6, 10)  # Cavalry has a slightly longer attack range than Soldier
        attack_strength = random.uniform(45, 60)  # Cavalry's attack strength
        agents.append(Agent("A", "Cavalry", position, health, attack_range, attack_strength))

    # Create agents for team B
    for _ in range(num_archers_b):
        position = (random.uniform(0, 200), random.uniform(0, 30))
        health = 80
        attack_range = random.uniform(30, 50)  # Archers have a longer attack range
        attack_strength = random.randint(15, 40)  # Archers hit less hard
        agents.append(Agent("B", "Archer", position, health, attack_range, attack_strength))

    for _ in range(num_soldiers_b):
        position = (random.uniform(0, 200), random.uniform(30, 60))
        health = 100
        attack_range = random.uniform(1, 5)  # Archers have a longer attack range
        attack_strength = random.randint(20, 30)  # Archers hit less hard
        agents.append(Agent("B", "Soldier", position, health, attack_range, attack_strength))

    for _ in range(num_cavalry_b):
        position = (random.uniform(0, 200), random.uniform(70, 100))  # Adjust position as desired
        health = 150
        attack_range = random.uniform(2, 8)  # Cavalry has a slightly longer attack range than Soldier
        attack_strength = random.uniform(45, 60)  # Cavalry's attack strength
        agents.append(Agent("B", "Cavalry", position, health, attack_range, attack_strength))

    # Initialize figure and counter for visualization
    fig, ax = plt.subplots()
    counter = ax.text(8, 9.5, f"Agents B: {num_agents_b}", fontsize=12, ha='right')


    #agents_active_list = []
    # Simulation loop
    for step in range(max_steps):
        # Iterate over all agents
        # Check if step is over 40, if yes, reset retreat behavior
        if step > 40:
            retreat_point = None
        else:
            retreat_point = (100, 100)

        formation_a, formation_b = create_formations(agents)
        
        active_agents = len(agents)
        for agent in agents:
            # Find the nearest enemy agent from the opposite team
            nearest_enemy = min([a for a in agents if a.team != agent.team], key=lambda a: agent.distance_to(a))

            # Get agents in range of the current agent
            agents_in_range = agent.get_agents_in_range(agents, agent.attack_range)
            
            if agent.agent_type == 'A':
                num_friends, num_enemies = agent.count_friends_and_enemies(agents_in_range)
                if step < 40:
                    common_point = (100, 150)  # The common point is the center of the map (you can adjust it as desired)
                    agent.retreat_to_common_point(agents, common_point)
                    enemy_formation = formation_b if agent.team == 'A' else formation_a
                    enemy_formation_positions = [a.position for a in enemy_formation]
                    common_point = calculate_centroid(enemy_formation_positions)

                    agent.retreat_to_common_point(agents, common_point)

                if retreat_point is not None:
                        agent.retreat_to_common_point(agents, retreat_point)  # Retreat behavior to (100, 100)

            if agent.agent_type == 'B':
                num_friends, num_enemies = agent.count_friends_and_enemies(agents_in_range)
                if num_enemies > num_friends:
                    common_point = (100, 50)  # The common point is the center of the map (you can adjust it as desired)
                    agent.retreat_to_common_point(agents, common_point)
                    

            elif agent.agent_type == 'Soldier' or agent.agent_type == 'Cavalry':
                # Move towards the nearest enemy agent
                dx = nearest_enemy.position[0] - agent.position[0]
                dy = nearest_enemy.position[1] - agent.position[1]
                dx /= agent.distance_to(nearest_enemy)
                dy /= agent.distance_to(nearest_enemy)
                agent.position = (agent.position[0] + dx, agent.position[1] + dy)

                # Attack if an enemy is within the agent's attack range
                if agent.distance_to(nearest_enemy) <= agent.attack_range:
                    agent.attack(nearest_enemy)
                    if nearest_enemy.health <= 0:
                        agents.remove(nearest_enemy)
                        print(f"{nearest_enemy.team} {nearest_enemy.agent_type} died!")
                        if agent.team == "A":
                            deaths_B[step + 1] += 1  # Increment deaths counter for Team B
                            with open('deaths_team_b.csv', 'a') as file:
                                file.write(f"{step + 1},{deaths_B[step + 1]}\n")
                        elif agent.team == "B":
                            deaths_A[step + 1] += 1  # Increment deaths counter for Team A
                            with open('deaths_team_a.csv', 'a') as file:
                                file.write(f"{step + 1},{deaths_A[step + 1]}\n")

        #   active_agents_list.append(active_agents)
        #  with open('active_agents.csv', 'a') as file:
        #     file.write(f"{step + 1},{active_agents[step + 1]}\n")
        # Clear the previous frame
        ax.clear()

        # Plot agents
        for agent in agents:
            if agent.team == 'A':
                color = 'red' if agent.agent_type == 'Archer' else 'salmon' if agent.agent_type == 'Soldier' else 'indianred'  # Archers: red, Soldiers: salmon, Cavalry: indianred
                marker = '^' if agent.agent_type == 'Archer' else 'X' if agent.agent_type == 'Soldier' else 's'  # Archers: ^, Soldiers: X, Cavalry: s
            if agent.team == "B":
                color = 'blue' if agent.agent_type == 'Archer' else 'lightblue' if agent.agent_type == 'Soldier' else 'royalblue'  # Archers: blue, Soldiers: lightblue, Cavalry: royalblue
                marker = 'v' if agent.agent_type == 'Archer' else 'o' if agent.agent_type == 'Soldier' else 'D'  # Archers: v, Soldiers: o, Cavalry: D
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

    # Check winning team and display message
    remaining_agents_a = len([agent for agent in agents if agent.team == 'A'])
    remaining_agents_b = len([agent for agent in agents if agent.team == 'B'])
    if remaining_agents_a == 0:
        print("Team B won!")
    elif remaining_agents_b == 0:
        print("Team A won!")

    # Display the final plot
    plt.show()

if __name__ == "__main__":
    main()
