import math
import random
import matplotlib.pyplot as plt
import argparse
import numpy as np

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
    
    def distance_to_agent(self, agent):
        return math.sqrt((self.position[0] - agent.position[0])**2 + (self.position[1] - agent.position[1])**2)

    def distance_to(self, agents):
        return math.sqrt((self.position[0] - nearest_enemy.position[0])**2 + (self.position[1] - nearest_enemy.position[1])**2)

    def attack(self, nearest_enemy):
        nearest_enemy.health -= self.attack_strength
        print(f"{self.team} {self.agent_type} attacked {nearest_enemy.team} {nearest_enemy.agent_type}!")

    def min_health_of_opponents(self, other_agents):
        return min(agent.health for agent in other_agents if agent.team != self.team)

    def get_agents_in_range(self, agents, range_distance):
        return [agent for agent in agents if agent != self and self.distance_to_agent(agent) <= 40]#range_distance]

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

def main():

    def calculate_centroid(positions):
        num_positions = len(positions)
        if num_positions == 0:
            return (0, 0)
        sum_x = sum(pos[0] for pos in positions)
        sum_y = sum(pos[1] for pos in positions)
        return (sum_x / num_positions, sum_y / num_positions)

    def parse_arguments():
        parser = argparse.ArgumentParser(description='Simulate a battle between two teams with infantry and cavalry.')
        parser.add_argument('--num_infantry', type=int, default=250, help='Number of infantry per team')
        parser.add_argument('--num_cavalry', type=int, default=125, help='Number of cavalry per team')
        return parser.parse_args()

    
    # Simulation parameters
    args = parse_arguments()
    num_infantry_a = args.num_infantry // 2
    num_cavalry_a = args.num_cavalry // 2
    num_agents_a = num_infantry_a + num_cavalry_a
    num_agents_b = args.num_infantry - num_infantry_a + args.num_cavalry - num_cavalry_a
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
    num_cavalry_a = num_agents_a // 2
    num_agents_b = num_agents - num_agents_a
    num_infantry_b = num_agents_b // 2
    num_cavalry_b = num_agents_b // 4  # Assuming 1/4 of Team B agents are Cavalry

    
    def create_agents_in_region(agents_list, team, agent_type, num_agents, region_boundary):
        region_left, region_right, region_top, region_bottom = region_boundary
        for _ in range(num_agents):
            if agent_type == "Infantry":
                position = (random.uniform(region_left, region_right), random.uniform(region_bottom, region_top))
                health = 100
                attack_range = random.uniform(1, 50)
                attack_strength = random.uniform(20, 30)
            elif agent_type == "Cavalry":
                position = (random.uniform(region_left, region_right), random.uniform(region_bottom, region_top))
                health = 150
                attack_range = random.uniform(2, 8)
                attack_strength = random.uniform(1, 10)

            agents_list.append(Agent(team, agent_type, position, health, attack_range, attack_strength))


    #Range of the formations
    # Define the regions for archers as lists containing boundary coordinates
    region_1 = [0, 50, 180, 160]
    region_2 = [80, 120, 180, 160]
    region_3 = [150, 200, 180, 160]
    # Define the regions for soldiers as lists containing boundary coordinates
    region_4 = [0, 90, 150, 130]
    region_5 = [110, 200, 150, 130]

            
    #Create Agents in formations: A
    create_agents_in_region(agents, "A", "Soldier", num_soldiers_a // 2, region_1)
    create_agents_in_region(agents, "A", "Soldier", num_soldiers_a // 2, region_2)
    
    # Create cavalry in the first three regions
    create_agents_in_region(agents, "A", "Cavalry", num_cavalry_a // 3, region_3)
    create_agents_in_region(agents, "A", "Cavalry", num_cavalry_a // 3, region_4)
    create_agents_in_region(agents, "A", "Cavalry", num_cavalry_a // 3, region_5)


    def create_formations(agents):
        infantry_a = [agent for agent in agents if agent.team == 'A' and agent.agent_type == 'Infantry']
        cavalry_a = [agent for agent in agents if agent.team == 'A' and agent.agent_type == 'Cavalry']
        
        infantry_b = [agent for agent in agents if agent.team == 'B' and agent.agent_type == 'Infantry']
        cavalry_b = [agent for agent in agents if agent.team == 'B' and agent.agent_type == 'Cavalry']
        
        formation_a = infantry_a + cavalry_a
        formation_b = infantry_b + cavalry_b
        
        return formation_a, formation_b

    # Game Theory implementation
    players = ["A", "B"]
    strategies = {
        "A": ["Attack", "Defend"],
        "B": ["Attack", "Defend"]
    }
    
    # Define the payoff matrix (using random values, change later)
    payoff_matrix = {
        ("Attack", "Attack"): np.array([[100, 50], [50, 100]]),
        ("Attack", "Defend"): np.array([[70, 20], [10, 40]]),
        ("Defend", "Attack"): np.array([[40, 10], [20, 70]]),
        ("Defend", "Defend"): np.array([[50, 50], [50, 50]])
    }
    
    # Function to get the best response strategy for a player
    def get_best_response(player, opponent_strategy):
        best_response_index = np.argmax(payoff_matrix[(player, opponent_strategy)][:, player_map[player]])
        return strategies[player][best_response_index]
    
    
    #Create agents for team B
    for _ in range(num_infantry_b):
        position = (random.uniform(0, 200), random.uniform(0, 40))
        health = 100
        attack_range = random.uniform(1, 50)
        attack_strength = random.uniform(20, 30)
        agents.append(Agent("B", "Infantry", position, health, attack_range, attack_strength))

    for _ in range(num_cavalry_b):
        position = (random.uniform(0, 200), random.uniform(80, 60))
        health = 150
        attack_range = random.uniform(2, 8)
        attack_strength = random.uniform(20, 50)
        agents.append(Agent("B", "Cavalry", position, health, attack_range, attack_strength))

        
    # Create a scatter plot with subplots
    fig, ax = plt.subplots()
    counter = ax.text(0.02, 0.95, '', transform=ax.transAxes, color='red')
    
    #Simulation loop
    for step in range(max_steps):
        print(f"Agents in team A: {num_agents_a}")
        print(f"Infantry in team A: {num_infantry_a}")
        print(f"Cavalry in team A: {num_cavalry_a}")
        print(f"Agents in team B: {num_agents_a}")
        print(f"Infantry in team B: {num_infantry_a}")
        print(f"Cavalry in team B: {num_cavalry_a}")
        for agent in agents:
            nearest_enemy = min([a for a in agents if a.team != agent.team], key=lambda a: agent.distance_to_agent(a), default=None)
            #print("where each nearest enemy debugging starts")
            #print(nearest_enemy)
            #print(dir(nearest_enemy))
            #print(type(nearest_enemy))
            if nearest_enemy is None:
                continue  # No enemies nearby, so skip the current agent's turn
            
            agents_in_range = agent.get_agents_in_range(agents, agent.attack_range)


            if agent.agent_type == 'Infantry':
                if nearest_enemy.health > 0:
                    if agent.distance_to_agent(nearest_enemy) <= agent.attack_range:
                        agent.attack(nearest_enemy)
                        if nearest_enemy.health <= 0:
                            agents.remove(nearest_enemy)
                            print(f"{nearest_enemy.team} {nearest_enemy.agent_type} died!")
                            if agent.team == "A":
                                deaths_B[step + 1] += 1  # Increment deaths counter for Team B
                                with open('deaths_team_b_gettysburg.csv', 'a') as file:
                                    file.write(f"{step + 1},{deaths_B[step + 1]}\n")
                            elif agent.team == "B":
                                deaths_A[step + 1] += 1  # Increment deaths counter for Team A
                                with open('deaths_team_a_gettysburg.csv', 'a') as file:
                                    file.write(f"{step + 1},{deaths_A[step + 1]}\n")
                            
                    else:
                        dx = agent.position[0] - nearest_enemy.position[0]
                        dy = agent.position[1] - nearest_enemy.position[1]
                        dx /= agent.distance_to_agent(nearest_enemy)  # Corrected line here
                        dy /= agent.distance_to_agent(nearest_enemy)  # Corrected line here
                        agent.position = (agent.position[0] - dx, agent.position[1] - dy)
                elif agent.team == 'A':
                    num_friends, num_enemies = agent.count_friends_and_enemies(agents_in_range)
                    if num_enemies > num_friends:
                        common_point = (100, 150)
                        agent.retreat_to_common_point(agents, common_point)
                        enemy_formation = formation_b if agent.team == 'A' else formation_a
                        enemy_formation_positions = [a.position for a in enemy_formation]
                        common_point = calculate_centroid(enemy_formation_positions)
                        agent.retreat_to_common_point(agents, common_point)

                elif agent.team == 'B':
                    num_friends, num_enemies = agent.count_friends_and_enemies(agents_in_range)
                    if num_enemies > num_friends:
                        common_point = (100, 50)
                        agent.retreat_to_common_point(agents, common_point)
                        
            if agent.agent_type == 'Cavalry':
                if nearest_enemy.health > 0:
                    if agent.distance_to_agent(nearest_enemy) <= agent.attack_range:
                        agent.attack(nearest_enemy)
                        if nearest_enemy.health <= 0:
                            agents.remove(nearest_enemy)
                            print(f"{nearest_enemy.team} {nearest_enemy.agent_type} died!")
                            if agent.team == "A":
                                deaths_B[step + 1] += 1  # Increment deaths counter for Team B
                                with open('deaths_team_b_gettysburg.csv', 'a') as file:
                                    file.write(f"{step + 1},{deaths_B[step + 1]}\n")
                            elif agent.team == "B":
                                deaths_A[step + 1] += 1  # Increment deaths counter for Team A
                                with open('deaths_team_a_gettysburg.csv', 'a') as file:
                                    file.write(f"{step + 1},{deaths_A[step + 1]}\n")

                            
                    else:
                        dx = agent.position[0] - nearest_enemy.position[0]
                        dy = agent.position[1] - nearest_enemy.position[1]
                        dx /= agent.distance_to_agent(nearest_enemy)  # Corrected line here
                        dy /= agent.distance_to_agent(nearest_enemy)  # Corrected line here
                        agent.position = (agent.position[0] - dx, agent.position[1] - dy)
                elif agent.team == 'A':
                    num_friends, num_enemies = agent.count_friends_and_enemies(agents_in_range)
                    if num_enemies > num_friends:
                        common_point = (100, 150)
                        agent.retreat_to_common_point(agents, common_point)
                        enemy_formation = formation_b if agent.team == 'A' else formation_a
                        enemy_formation_positions = [a.position for a in enemy_formation]
                        common_point = calculate_centroid(enemy_formation_positions)
                        agent.retreat_to_common_point(agents, common_point)
                    
                elif agent.team == 'B':
                    num_friends, num_enemies = agent.count_friends_and_enemies(agents_in_range)
                    if num_enemies > num_friends:
                        common_point = (100, 50)
                        agent.retreat_to_common_point(agents, common_point)
                            
            

        # Clear the previous frame
        ax.clear()
        
        # Plot agents
        for agent in agents:
            if agent.team == 'A':
                color = 'red' if agent.agent_type == 'Infantry' else 'salmon' if agent.agent_type == 'Cavalry' else 'indianred'
                marker = 'X' if agent.agent_type == 'Infantry' else 's'  # Infantry: X, Cavalry: s
            if agent.team == "B":
                color = 'blue' if agent.agent_type == 'Infantry' else 'lightblue' if agent.agent_type == 'Cavalry' else 'royalblue'
                marker = 'o' if agent.agent_type == 'Infantry' else 'D'  # Infantry: o, Cavalry: D
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
