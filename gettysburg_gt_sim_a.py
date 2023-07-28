import math
import random
import matplotlib.pyplot as plt
import argparse
import numpy as np
import pandas as pd



class AgentTeamA:
    def __init__(self, agent_type, position, health, attack_range, attack_strength, last_action):
        self.team = "A"
        self.agent_type = agent_type  # You should set the actual type later based on Infantry/Cavalry
        self.position = position
        self.health = health
        self.attack_range = attack_range
        self.attack_strength = attack_strength
        self.last_action = "Attack"

    def distance_to_agent(self, agent):
        return math.sqrt((self.position[0] - agent.position[0])**2 + (self.position[1] - agent.position[1])**2)

    def distance_to(self, position):
        return math.sqrt((self.position[0] - position[0])**2 + (self.position[1] - position[1])**2)

    def attack(self, nearest_enemy):
        nearest_enemy.health -= self.attack_strength

    def defend(self, agents_in_range):
        if not agents_in_range:
            common_point = (100, 150)
            self.retreat_to_common_point(common_point)

    def min_health_of_opponents(self, other_agents):
        return min(agent.health for agent in other_agents if agent.team != self.team)

    def get_agents_in_range(self, agents, range_distance):
        return [agent for agent in agents if agent != self and self.distance_to_agent(agent) <= range_distance]

    def count_friends_and_enemies(self, agents_in_range):
        friends = [agent for agent in agents_in_range if agent.team == self.team]
        enemies = [agent for agent in agents_in_range if agent.team != self.team]
        return len(friends), len(enemies)

    def retreat_to_common_point(self, common_point):
        dx = common_point[0] - self.position[0]
        dy = common_point[1] - self.position[1]
        distance_to_common_point = self.distance_to(common_point)
        if distance_to_common_point > 0:
            dx /= distance_to_common_point
            dy /= distance_to_common_point
            self.position = (self.position[0] - dx, self.position[1] - dy)

    def set_game_theory_info(self, strategies, payoff_matrix):
        AgentTeamA.strategies = strategies
        AgentTeamA.payoff_matrix = payoff_matrix

    def chosen_action(self, opponent_strategy):
        # NEW CODE (DELETE PROBABLY)
        new_interpret = {
            "Attack": "A",
            "Defend": "B"
        }
        new_interpret_b = {
            "Attack": "A",
            "Defend": "B"
        }
        #opponent_index = strategies[opponent_team].index(opponent_strategy)
        print("Agent team, opponent strategy")
        print((self.team, new_interpret[opponent_strategy]))
        best_response_index = np.argmax(self.payoff_matrix[(self.team, new_interpret[opponent_strategy])][:, self.players.index(self.team)])
        print(best_response_index)
        #best_response_action = strategies[self.team][best_response_index]
        #return best_response_action
        return self.strategies[self.team][best_response_index]

class AgentOpponentTeam:
    def __init__(self, agent_type, position, health, attack_range, attack_strength, last_action):
        self.team = "opponent"
        self.agent_type = agent_type  
        self.position = position
        self.health = health
        self.attack_range = attack_range
        self.attack_strength = attack_strength
        self.last_action = "Attack"

    def distance_to_agent(self, agent):
        return math.sqrt((self.position[0] - agent.position[0])**2 + (self.position[1] - agent.position[1])**2)

    def distance_to(self, position):
        return math.sqrt((self.position[0] - position[0])**2 + (self.position[1] - position[1])**2)

    def attack(self, nearest_enemy):
        nearest_enemy.health -= self.attack_strength

    def defend(self, agents_in_range):
        if not agents_in_range:
            common_point = (100, 50)  # Opponent team's common point (change as needed)
            self.retreat_to_common_point(common_point)

    def retreat_to_common_point(self, common_point):
        dx = common_point[0] - self.position[0]
        dy = common_point[1] - self.position[1]
        distance_to_common_point = self.distance_to(common_point)
        if distance_to_common_point > 0:
            dx /= distance_to_common_point
            dy /= distance_to_common_point
            self.position = (self.position[0] - dx, self.position[1] - dy)

    def get_agents_in_range(self, agents, range_distance):
        return [agent for agent in agents if agent != self and self.distance_to_agent(agent) <= range_distance]

    def count_friends_and_enemies(self, agents_in_range):
        friends = [agent for agent in agents_in_range if agent.team == self.team]
        enemies = [agent for agent in agents_in_range if agent.team != self.team]
        return len(friends), len(enemies)

    def set_game_theory_info(self, strategies, payoff_matrix):
        AgentTeamA.strategies = strategies
        AgentTeamA.payoff_matrix = payoff_matrix
    
    def chosen_action(self, opponent_strategy):
        # NEW CODE (DELETE PROBABLY)
        new_interpret = {
            "Attack": "A",
            "Defend": "B"
        }
        opponent_index = team_a_strategies.index(opponent_strategy)
        print("Agent team, opponent strategy")
        print((self.team, new_interpret[opponent_strategy]))
        best_response_index = np.argmax(self.payoff_matrix[(self.team, new_interpret[opponent_strategy])][:, self.players.index(self.team)])
        print(best_response_index)
        best_response_action = strategies[self.team][best_response_index]
        return best_response_action
        #return self.strategies[self.team][best_response_index]




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

    agents_team_a = []
    agents_opponent_team = []
    num_agents_a = num_agents // 2
    num_soldiers_a = num_agents_a // 2
    num_cavalry_a = num_agents_a // 2
    num_agents_opponent = num_agents - num_agents_a
    num_infantry_opponent = num_agents_opponent // 2
    num_cavalry_opponent = num_agents_opponent // 4

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

            agents_list.append(AgentTeamA(team, agent_type, position, health, attack_range, attack_strength))

    region_1 = [0, 50, 180, 160]
    region_2 = [80, 120, 180, 160]
    region_3 = [150, 200, 180, 160]
    region_4 = [0, 90, 150, 130]
    region_5 = [110, 200, 150, 130]

    create_agents_in_region(agents_team_a, "A", "Soldier", num_soldiers_a // 2, region_1)
    create_agents_in_region(agents_team_a, "A", "Soldier", num_soldiers_a // 2, region_2)
    create_agents_in_region(agents_team_a, "A", "Cavalry", num_cavalry_a // 3, region_3)
    create_agents_in_region(agents_team_a, "A", "Cavalry", num_cavalry_a // 3, region_4)
    create_agents_in_region(agents_team_a, "A", "Cavalry", num_cavalry_a // 3, region_5)

    def create_formations(agents):
        infantry_a = [agent for agent in agents if agent.team == 'A' and agent.agent_type == 'Infantry']
        cavalry_a = [agent for agent in agents if agent.team == 'A' and agent.agent_type == 'Cavalry']
        infantry_opponent = [agent for agent in agents if agent.team == 'B' and agent.agent_type == 'Infantry']
        cavalry_opponent = [agent for agent in agents if agent.team == 'B' and agent.agent_type == 'Cavalry']
        formation_a = infantry_a + cavalry_a
        formation_opponent = infantry_opponent + cavalry_opponent
        return formation_a, formation_opponent

    players = ["A", "B"]

    strategies_team_a = {
        "A": ["Attack"],
        "B": ["Attack"]
    }

    strategies_opponent_team = {
        "A": ["Attack"],
        "B": ["Attack"]
    }

    payoff_matrix_team_a = {
        ("A", "A"): np.array([[100]]),
        ("A", "B"): np.array([[70]]),
        ("B", "A"): np.array([[40]]),
        ("B", "B"): np.array([[50]])
    }

    payoff_matrix_opponent_team = {
        ("A", "A"): np.array([[50]]),
        ("A", "B"): np.array([[20]]),
        ("B", "A"): np.array([[10]]),
        ("B", "B"): np.array([[50]])
    }

    AgentTeamA.set_game_theory_info(agents_team_a, strategies_team_a, payoff_matrix_team_a)
    AgentOpponentTeam.set_game_theory_info(agents_opponent_team, strategies_opponent_team, payoff_matrix_opponent_team)

    # Create instances of AgentOpponentTeam for opponent team agents
    for _ in range(num_infantry_opponent):
        position = (random.uniform(0, 200), random.uniform(0, 40))
        health = 100
        attack_range = random.uniform(1, 50)
        attack_strength = random.uniform(20, 30)
        AgentOpponentTeam.set_game_theory_info(agents_opponent_team, strategies_opponent_team, payoff_matrix_opponent_team)

    for _ in range(num_cavalry_opponent):
        position = (random.uniform(0, 200), random.uniform(80, 60))
        health = 150
        attack_range = random.uniform(2, 8)
        attack_strength = random.uniform(20, 50)
        AgentOpponentTeam.set_game_theory_info(agents_opponent_team, strategies_opponent_team, payoff_matrix_opponent_team)

    agent_movements = []
    agent_movements = pd.DataFrame({
        "Step": step,
        "Team": team,
        "Agent_Type": agent_type,
        "X": agent_position[0],
        "Y": agent_position[1]
    })

    for step in range(max_steps):
        for agent_team_a in agents_team_a:
            nearest_enemy = min(agents_opponent_team, key=lambda a: agent_team_a.distance_to_agent(a), default=None)
            if nearest_enemy is None:
                continue
            agents_in_range = agent_team_a.get_agents_in_range(agents_opponent_team, agent_team_a.attack_range)

            if agent_team_a.agent_type == 'Infantry':
                opponent_strategy = nearest_enemy.last_action
                chosen_action = agent_team_a.chosen_action(AgentTeamA.strategies['A'],
                                                           AgentTeamA.payoff_matrix,
                                                           opponent_strategy)
                if chosen_action == "Attack":
                    if nearest_enemy.health > 0 and agent_team_a.distance_to_agent(nearest_enemy) <= agent_team_a.attack_range:
                        agent_team_a.attack(nearest_enemy)
                        if nearest_enemy.health <= 0:
                            agents_opponent_team.remove(nearest_enemy)
                            deaths_B[step + 1] += 1
                            with open('deaths_team_b_gettysburg.csv', 'a') as file:
                                file.write(f"{step + 1},{deaths_B[step + 1]}\n")
                elif chosen_action == "Defend":
                    num_friends, num_enemies = agent_team_a.count_friends_and_enemies(agents_in_range)
                    if num_enemies > num_friends:
                        common_point = (100, 150)
                        agent_team_a.retreat_to_common_point(common_point)
                        if nearest_enemy.health > 0:
                            if agent_team_a.distance_to_agent(nearest_enemy) <= agent_team_a.attack_range:
                                agent_team_a.attack(nearest_enemy)
                                if nearest_enemy.health <= 0:
                                    agents_opponent_team.remove(nearest_enemy)
                                    deaths_B[step + 1] += 1
                                    with open('deaths_team_b_gettysburg.csv', 'a') as file:
                                        file.write(f"{step + 1},{deaths_B[step + 1]}\n")

            elif agent_team_a.agent_type == 'Cavalry':
                opponent_strategy = nearest_enemy.last_action
                chosen_action = agent_team_a.chosen_action(AgentTeamA.strategies['A'],
                                                           AgentTeamA.payoff_matrix,
                                                           opponent_strategy)
                if chosen_action == "Attack":
                    if nearest_enemy.health > 0 and agent_team_a.distance_to_agent(nearest_enemy) <= agent_team_a.attack_range:
                        agent_team_a.attack(nearest_enemy)
                        if nearest_enemy.health <= 0:
                            agents_opponent_team.remove(nearest_enemy)
                            deaths_B[step + 1] += 1
                            with open('deaths_team_b_gettysburg.csv', 'a') as file:
                                file.write(f"{step + 1},{deaths_B[step + 1]}\n")
                elif chosen_action == "Defend":
                    num_friends, num_enemies = agent_team_a.count_friends_and_enemies(agents_in_range)
                    if num_enemies > num_friends:
                        common_point = (100, 150)
                        agent_team_a.retreat_to_common_point(common_point)
                        if nearest_enemy.health > 0:
                            if agent_team_a.distance_to_agent(nearest_enemy) <= agent_team_a.attack_range:
                                agent_team_a.attack(nearest_enemy)
                                if nearest_enemy.health <= 0:
                                    agents_opponent_team.remove(nearest_enemy)
                                    deaths_B[step + 1] += 1
                                    with open('deaths_team_b_gettysburg.csv', 'a') as file:
                                        file.write(f"{step + 1},{deaths_B[step + 1]}\n")

            agent_team_a.last_action = chosen_action
    agent_movements = agent_movements.append({'Step': step + 1,
                                              'Team': agent.team,
                                              'AgentType': agent.agent_type,
                                              'X': agent.position[0],
                                              'Y': agent.position[1]}, ignore_index=True)


    agent_movements_df = pd.DataFrame(agent_movements)
    agent_movements_df.to_csv('agent_movements_gettysburg.csv', index=False)

if __name__ == "__main__":
    main()

