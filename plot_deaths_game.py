import csv
import matplotlib.pyplot as plt

# Function to read deaths from CSV file
def read_deaths(filename):
    steps = []
    deaths = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            steps.append(int(row[0]))
            deaths.append(int(row[1]))
    return steps, deaths

# Read deaths for Team A and Team B
steps_a, deaths_a = read_deaths('deaths_team_a.csv')
steps_b, deaths_b = read_deaths('deaths_team_b.csv')

# Plot deaths per step for Team A in red
plt.plot(steps_a, deaths_a, marker='o', linestyle='-', color='r', label='Team A')

# Plot deaths per step for Team B in blue
plt.plot(steps_b, deaths_b, marker='o', linestyle='-', color='b', label='Team B')

plt.xlabel('Step')
plt.ylabel('Deaths')
plt.title('Deaths per Step')
plt.legend()
plt.grid(True)
plt.show()
