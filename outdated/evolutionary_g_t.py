import random
import nashpy as nash

class Empire:
    def __init__(self, name, military_strength, economic_resources, population):
        self.name = name
        self.control = random.uniform(0, 1)
        self.military_strength = military_strength
        self.economic_resources = economic_resources
        self.population = population

    def evolve(self, other_empire):
        # Calculate the control change based on military strength, economic resources, and population dynamics
        military_factor = 0.5
        economic_factor = 0.4
        population_factor = 0.2

        control_change = (
            (self.military_strength * military_factor)
            + (self.economic_resources * economic_factor)
            + (self.population * population_factor)
            - (other_empire.military_strength * military_factor)
            - (other_empire.economic_resources * economic_factor)
            - (other_empire.population * population_factor)
        )

        control_change += random.uniform(-0.5, 0.5)  # Add a random control change within a range

        # Adjust control change based on historical dominance of empires
        dominance_factor = 0.2
        if self.control > other_empire.control:
            control_change += dominance_factor
        elif self.control < other_empire.control:
            control_change -= dominance_factor

        # Apply control change
        self.control = max(min(self.control + control_change, 1), 0)  # Control limited between 0 and 1

        return self.control

# Create empires with verified statistics
spanish_military_strength = 500000  # Approximate number of soldiers
spanish_economic_resources = 3000  # Approximate annual revenue in thousands of ducats
spanish_population = 8500000  # Approximate population in millions

british_military_strength = 30000  # Approximate number of soldiers
british_economic_resources = 1000  # Approximate annual revenue in thousands of pounds
british_population = 4000000  # Approximate population in millions

# Define the payoff matrix based on control levels
payoff_matrix = [[0, 1], [1, 0]]  # Placeholder values for the payoff matrix

# Create empires with verified statistics
spanish_empire = Empire("Spanish Control", spanish_military_strength, spanish_economic_resources, spanish_population)
british_empire = Empire("British Control", british_military_strength, british_economic_resources, british_population)

# Historical control data
historical_data = {
    "Spanish Control": [],
    "British Control": []
}

# Play multiple time periods of competition
num_periods = 100
for period in range(num_periods):
    # Empires evolve and update their control
    spanish_control = spanish_empire.evolve(british_empire)
    british_control = british_empire.evolve(spanish_empire)

    # Update historical data for the next period
    historical_data["Spanish Control"].append(spanish_control)
    historical_data["British Control"].append(british_control)

    # Print control levels for each period
    print(f"Period {period + 1}:")
    print("Spanish Control:", spanish_control)
    print("British Control:", british_control)

    # Find and print the Nash equilibria of the control game
    payoff_matrix[0][0] = spanish_control
    payoff_matrix[0][1] = british_control
    payoff_matrix[1][0] = british_control
    payoff_matrix[1][1] = spanish_control

    control_game = nash.Game(payoff_matrix)
    nash_equilibria = control_game.support_enumeration()
    for eq in nash_equilibria:
        strategy_spanish, strategy_british = eq
        print("Nash Equilibrium Strategies:")
        print("Spanish Empire Strategy:", strategy_spanish)
        print("British Empire Strategy:", strategy_british)

    print("------------------")
    
