import math
import random
import matplotlib.pyplot as plt
import argparse
import numpy as np
import pandas as pd

#To run: python3 gettysburg_gt_sim_a.py --num_infantry 300 --num_infantry 200
#Also need to account for Cemetery Hill...(last stand of the union)
#Plan is to make the union retreat to common point while still being close to confederates, as to simulate actual battle, then all out attack at cemetery hill, which was the start of the demise of the confederate armyot

#Todo al 10% de la batalla actual
#Cambiar como se crean los agentes para estar a raya con el campo actual


def main():
    agent_opponent_team = AgentOpponentTeam(agent_type, position, health, attack_range, attack_strength, last_action)
    max_steps = 1000
    battlefield = Battlefield(2000, 1000)
    battlefield.set_region(400, 600, 700, 900, 1)  #This is where the agents from the union gave their last stand and won the battle
    run_game_logic(agent_opponent_team, max_steps)
    
def parse_arguments():
    parser = argparse.ArgumentParser(description='Simulate a battle between two teams with infantry and cavalry.')
    parser.add_argument('--num_infantry', type=int, default=250, help='Number of infantry per team')
    parser.add_argument('--num_cavalry', type=int, default=125, help='Number of cavalry per team')
    return parser.parse_args()
    
def setup_battle():
    
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


def run_game_logic(agents_team_a, agents_opponent_team, max_steps):
    setup_battle()
    for step in range(max_steps):
        # Team A chooses its actions
        for agent_team_a in agents_team_a:
            # For example, Team A decides whether to Attack or Defend based on the situation
            if step < 300:
                chosen_action = "Defend"  # Higher payoff for Defend if step < 300
            elif 201 <= step <=600:
                pass#Let it choose
            else:
                chosen_action = "Attack"
            # Perform actions based on the chosen action for Team A
            if agent_team_a.agent_type == "Infantry":
                a_infantry_actions(agent_team_a, chosen_action)
            elif agent_team_a.agent_type == "Cavalry":
                a_cavalry_actions(agent_team_a, chosen_action)

        # Opponent Team always attacks, so no need to choose actions for them
        chosen_action_opponent = "Attack"



class AgentTeamA:
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

#Common point will be Cemetery hill, maybe put all of the actions into a new file??
def a_infantry_actions(chosen_action):
        nearest_enemy = min(agents_opponent_team, key=lambda a: agent_team_a.distance_to_agent(a), default=None)
        agents_in_range = agent_team_a.get_agents_in_range(agents_opponent_team, agent_team_a.attack_range)
        opponent_strategy = nearest_enemy.last_action
        chosen_action = agent_team_a.chosen_action(AgentTeamA.strategies['A'], AgentTeamA.payoff_matrix, opponent_strategy)
        
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

def a_cavalry_actions(chosen_action):
    nearest_enemy = min(agents_opponent_team, key=lambda a: agent_team_a.distance_to_agent(a), default=None)
    agents_in_range = agent_team_a.get_agents_in_range(agents_opponent_team, agent_team_a.attack_range)
    opponent_strategy = nearest_enemy.last_action
    chosen_action = agent_team_a.chosen_action(AgentTeamA.strategies['A'], AgentTeamA.payoff_matrix, opponent_strategy)
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

def o_infantry_actions(chosen_action):
        nearest_enemy = min(agents_team_a, key=lambda a: agent_opponent_team.distance_to_agent(a), default=None)
        agents_in_range = agent_opponent_team.get_agents_in_range(agents_team_a, agent_opponent_team.attack_range)
        opponent_strategy = nearest_enemy.last_action
        chosen_action = agent_opponent_team.chosen_action(AgentTeamA.strategies['A'], AgentTeamA.payoff_matrix, opponent_strategy)
        if nearest_enemy.health > 0 and agent_opponent_team.distance_to_agent(nearest_enemy) <= agent_opponent_team.attack_range:
            agent_team_a.attack(nearest_enemy)
            if nearest_enemy.health <= 0:
                agents_team_a.remove(nearest_enemy)
                deaths_A[step + 1] += 1
                with open('deaths_team_a_gettysburg.csv', 'a') as file:
                    file.write(f"{step + 1},{deaths_A[step + 1]}\n")


def o_cavalry_actions(chosen_action):
        nearest_enemy = min(agents_team_a, key=lambda a: agent_opponent_team.distance_to_agent(a), default=None)
        agents_in_range = agent_opponent_team.get_agents_in_range(agents_team_a, agent_opponent_team.attack_range)
        opponent_strategy = nearest_enemy.last_action
        chosen_action = agent_opponent_team.chosen_action(AgentTeamA.strategies['A'], AgentTeamA.payoff_matrix, opponent_strategy)
            if nearest_enemy.health > 0 and agent_opponent_team.distance_to_agent(nearest_enemy) <= agent_opponent_team.attack_range:
                agent_opponent_team.attack(nearest_enemy)
                if nearest_enemy.health <= 0:
                    agents_team_a.remove(nearest_enemy)
                    deaths_A[step + 1] += 1
                    with open('deaths_team_a_gettysburg.csv', 'a') as file:
                        file.write(f"{step + 1},{deaths_A[step + 1]}\n")
##########################################################################################
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
        AgentOpponentTeam.strategies = strategies
        AgentOppnentTeam.payoff_matrix = payoff_matrix
    
    def chosen_action(self, opponent_strategy):
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

###########################################################################################
class Battlefield:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

    def set_region(self, x1, y1, x2, y2, value):
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                if 0 <= x < self.cols and 0 <= y < self.rows:
                    self.grid[y][x] = value

    def get_cell_value(self, x, y):
        if 0 <= x < self.cols and 0 <= y < self.rows:
            return self.grid[y][x]
        return None


main()
