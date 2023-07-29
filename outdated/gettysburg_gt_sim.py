import math
import random
import matplotlib.pyplot as plt
import argparse
import numpy as np
import pandas as pd

class Agent:
    def __init__(self, team, agent_type, position, health, attack_range, attack_strength):
        # NEW CODE (DELETE PROBABLY)
        self.players = ["A", "B"]
        self.strategies = {
            "A": ["Attack", "Defend"],
            "B": ["Attack", "Defend"]
        }
        ###########################
        self.team = team
        self.agent_type = agent_type
        self.position = position
        self.health = health
        self.attack_range = attack_range
        self.attack_strength = attack_strength
        self.last_action = "Attack"

    payoff_matrix = None
    
    def distance_to_agent(self, agent):
        return math.sqrt((self.position[0] - agent.position[0])**2 + (self.position[1] - agent.position[1])**2)

    def distance_to(self, agents):
        return math.sqrt((self.position[0] - nearest_enemy.position[0])**2 + (self.position[1] - nearest_enemy.position[1])**2)

    def attack(self, nearest_enemy):
        nearest_enemy.health -= self.attack_strength

    def defend(self, nearest_enemy):
        if not agents_in_range:
            if self.team == 'A':
                common_point = (100, 150)
            else:
                common_point = (100, 50)
            self.retreat_to_common_point(agents, common_point)

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

    def set_game_theory_info(self, players, strategies, payoff_matrix):
        Agent.payoff_matrix = payoff_matrix


    def chosen_action(self, opponent_strategy):
        # NEW CODE (DELETE PROBABLY)
        new_interpret = {
            "Attack": "A",
            "Defend": "B"
        }
        print((self.team, new_interpret[opponent_strategy]))
        best_response_index = np.argmax(self.payoff_matrix[(self.team, new_interpret[opponent_strategy])][:, self.players.index(self.team)])
        ###################################################
        print(best_response_index)
        return self.strategies[self.team][best_response_index]

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

    agents = []
    num_agents_a = num_agents // 2
    num_soldiers_a = num_agents_a // 2
    num_cavalry_a = num_agents_a // 2
    num_agents_b = num_agents - num_agents_a
    num_infantry_b = num_agents_b // 2
    num_cavalry_b = num_agents_b // 4

    def create_agents_in_region(agents_list, team, agent_type, num_agents, region_boundary):
        region_left, region_right, region_top, region_bottom = region_boundary
        for _ in range(num_agents):
            if agent_type == "Infantry":
                position = (random.uniform(region_left, region_right), random.uniform(region_bottom, region_top))
                health = 100
                attack_range = random.uniform(1, 50)
                attack_strength = random.uniform(20, 30)
            else:
                position = (random.uniform(region_left, region_right), random.uniform(region_bottom, region_top))
                health = 150
                attack_range = random.uniform(2, 8)
                attack_strength = random.uniform(1, 10)

            agents_list.append(Agent(team, agent_type, position, health, attack_range, attack_strength))

    region_1 = [0, 50, 180, 160]
    region_2 = [80, 120, 180, 160]
    region_3 = [150, 200, 180, 160]
    region_4 = [0, 90, 150, 130]
    region_5 = [110, 200, 150, 130]

    create_agents_in_region(agents, "A", "Soldier", num_soldiers_a // 2, region_1)
    create_agents_in_region(agents, "A", "Soldier", num_soldiers_a // 2, region_2)
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

    players = ["A", "B"]

    strategies = {
        "A": ["Attack", "Defend"],
        "B": ["Attack", "Defend"]
    }

    payoff_matrix = {
        ("A", "A"): np.array([[100, 50], [50, 100]]),
        ("A", "B"): np.array([[70, 20], [10, 40]]),
        ("B", "A"): np.array([[40, 10], [20, 70]]),
        ("B", "B"): np.array([[50, 50], [50, 50]])
    }

    Agent.set_game_theory_info(agents, strategies, payoff_matrix, payoff_matrix)

    
    def get_best_response(player, opponent_strategy):
        best_response_index = np.argmax(payoff_matrix[(player, opponent_strategy)][:, player_map[player]])
        return strategies[player][best_response_index]

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

    agent_movements = pd.DataFrame(columns=['Step', 'Team', 'AgentType', 'X', 'Y'])

    for step in range(max_steps):
        for agent in agents:
            nearest_enemy = min([a for a in agents if a.team != agent.team], key=lambda a: agent.distance_to_agent(a), default=None)
            if nearest_enemy is None:
                continue
            agents_in_range = agent.get_agents_in_range(agents, agent.attack_range)

            if agent.agent_type == 'Infantry':
                opponent_strategy = nearest_enemy.last_action
                chosen_action = agent.chosen_action(opponent_strategy)
                if chosen_action == "Attack":
                    if nearest_enemy.health > 0 and agent.distance_to_agent(nearest_enemy) <= agent.attack_range:
                        agent.attack(nearest_enemy)
                        if nearest_enemy.health <= 0:
                            agents.remove(nearest_enemy)
                            if agent.team == "A":
                                deaths_B[step + 1] += 1
                                with open('deaths_team_b_gettysburg.csv', 'a') as file:
                                    file.write(f"{step + 1},{deaths_B[step + 1]}\n")
                            elif agent.team == "B":
                                deaths_A[step + 1] += 1
                                with open('deaths_team_a_gettysburg.csv', 'a') as file:
                                    file.write(f"{step + 1},{deaths_A[step + 1]}\n")
                    else:
                        dx = agent.position[0] - nearest_enemy.position[0]
                        dy = agent.position[1] - nearest_enemy.position[1]
                        dx /= agent.distance_to_agent(nearest_enemy)
                        dy /= agent.distance_to_agent(nearest_enemy)
                        agent.position = (agent.position[0] - dx, agent.position[1] - dy)
                elif chosen_action == "Defend":
                    num_friends, num_enemies = agent.count_friends_and_enemies(agents_in_range)
                    if num_enemies > num_friends:
                        if agent.team == 'A':
                            common_point = (100, 150)
                        elif agent.team == 'B':
                            common_point = (100, 50)
                        agent.retreat_to_common_point(agents, common_point)
                        if nearest_enemy.health > 0:
                            if agent.distance_to_agent(nearest_enemy) <= agent.attack_range:
                                agent.attack(nearest_enemy)
                                if nearest_enemy.health <= 0:
                                    agents.remove(nearest_enemy)
                                    if agent.team == "A":
                                        deaths_B[step + 1] += 1
                                        with open('deaths_team_b_gettysburg.csv', 'a') as file:
                                            file.write(f"{step + 1},{deaths_B[step + 1]}\n")
                                    elif agent.team == "B":
                                        deaths_A[step + 1] += 1
                                        with open('deaths_team_a_gettysburg.csv', 'a') as file:
                                            file.write(f"{step + 1},{deaths_A[step + 1]}\n")
            elif agent.agent_type == 'Cavalry':
                opponent_strategy = nearest_enemy.last_action
                chosen_action = agent.chosen_action(opponent_strategy)
                if chosen_action == "Attack":
                    if nearest_enemy.health > 0 and agent.distance_to_agent(nearest_enemy) <= agent.attack_range:
                        agent.attack(nearest_enemy)
                        if nearest_enemy.health <= 0:
                            agents.remove(nearest_enemy)
                            if agent.team == "A":
                                deaths_B[step + 1] += 1
                                with open('deaths_team_b_gettysburg.csv', 'a') as file:
                                    file.write(f"{step + 1},{deaths_B[step + 1]}\n")
                            elif agent.team == "B":
                                deaths_A[step + 1] += 1
                                with open('deaths_team_a_gettysburg.csv', 'a') as file:
                                    file.write(f"{step + 1},{deaths_A[step + 1]}\n")
                    else:
                        dx = agent.position[0] - nearest_enemy.position[0]
                        dy = agent.position[1] - nearest_enemy.position[1]
                        dx /= agent.distance_to_agent(nearest_enemy)
                        dy /= agent.distance_to_agent(nearest_enemy)
                        agent.position = (agent.position[0] - dx, agent.position[1] - dy)
                elif chosen_action == "Defend":
                    num_friends, num_enemies = agent.count_friends_and_enemies(agents_in_range)
                    if num_enemies > num_friends:
                        if agent.team == 'A':
                            common_point = (100, 150)
                        elif agent.team == 'B':
                            common_point = (100, 50)
                        agent.retreat_to_common_point(agents, common_point)
                        if nearest_enemy.health > 0:
                            if agent.distance_to_agent(nearest_enemy) <= agent.attack_range:
                                agent.attack(nearest_enemy)
                                if nearest_enemy.health <= 0:
                                    agents.remove(nearest_enemy)
                                    if agent.team == "A":
                                        deaths_B[step + 1] += 1
                                        with open('deaths_team_b_gettysburg.csv', 'a') as file:
                                            file.write(f"{step + 1},{deaths_B[step + 1]}\n")
                                    elif agent.team == "B":
                                        deaths_A[step + 1] += 1
                                        with open('deaths_team_a_gettysburg.csv', 'a') as file:
                                            file.write(f"{step + 1},{deaths_A[step + 1]}\n")

    agent.last_action = chosen_action

    agent_movements = agent_movements.append({'Step': step + 1,
                                              'Team': agent.team,
                                              'AgentType': agent.agent_type,
                                              'X': agent.position[0],
                                              'Y': agent.position[1]}, ignore_index=True)

    agent_movements.to_csv('agent_movements_gettysburg.csv', index=False)

if __name__ == "__main__":
    main()
