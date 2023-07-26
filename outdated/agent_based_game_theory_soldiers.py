import random

# Define soldier class
class Soldier:
    def __init__(self, health, combat_skill):
        self.health = health
        self.combat_skill = combat_skill

    def attack(self):
        # Simulate combat skill-based attack
        return random.uniform(0, self.combat_skill)

    def select_target(self, other_soldiers):
        # Select a target based on combat skill comparison using game theory
        available_targets = [soldier for soldier in other_soldiers if soldier.health > 0]
        if available_targets:
            target = max(available_targets, key=lambda x: x.combat_skill)
        else:
            target = None
        return target

# Simulate a battle
def simulate_battle(num_soldiers):
    soldiers = []
    for _ in range(num_soldiers):
        health = random.uniform(80, 100)
        combat_skill = random.uniform(0.7, 1.0)
        soldiers.append(Soldier(health, combat_skill))

    # Run battle simulation
    num_rounds = 10
    for round in range(num_rounds):
        print(f"Round {round + 1}")

        # Determine actions for each soldier using game theory
        actions = []
        for i, soldier in enumerate(soldiers):
            target = soldier.select_target(soldiers[:i] + soldiers[i+1:])
            if target is not None and soldier.combat_skill > target.combat_skill:
                action = soldier.attack()
            else:
                action = 0.0  # No attack if target is stronger or no target available
            actions.append(action)

        # Calculate casualties and injuries based on actions
        total_casualties = 0
        total_injuries = 0
        for i in range(len(soldiers)):
            for j in range(i + 1, len(soldiers)):
                if actions[i] > actions[j]:
                    total_casualties += 1
                elif actions[i] < actions[j]:
                    total_injuries += 1

        print(f"Casualties: {total_casualties}")
        print(f"Injuries: {total_injuries}")
        print("------------------------")

# Run the battle simulation with 5 soldiers
simulate_battle(5)
