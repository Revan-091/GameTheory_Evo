import matplotlib.pyplot as plt

def plot_deaths_per_step(filename, team):
    # Read the deaths data from the CSV file
    with open(filename, 'r') as file:
        deaths = [int(line.strip()) for line in file]

    # Create the plot
    plt.plot(deaths, label=f'Team {team}')

# Plot the deaths data for each team
plot_deaths_per_step('deaths_team_a.csv', 'A')
plot_deaths_per_step('deaths_team_b.csv', 'B')

# Add labels and title
plt.xlabel('Step')
plt.ylabel('Deaths')
plt.title('Deaths per Step per Team')
plt.legend()

# Show the plot
plt.show()
