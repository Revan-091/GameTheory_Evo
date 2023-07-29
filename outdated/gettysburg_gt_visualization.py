import matplotlib.pyplot as plt

def visualize_movements(deaths_file, movements_file):
    # Read the deaths file
    with open(deaths_file, 'r') as file:
        lines = file.readlines()

    # Extract step and death counts from the deaths file
    steps = [int(line.strip().split(',')[0]) for line in lines]
    death_counts = [int(line.strip().split(',')[1]) for line in lines]

    # Read the movements file
    with open(movements_file, 'r') as file:
        lines = file.readlines()

    # Create a dictionary to store agent movements by step
    movements = {}
    for line in lines:
        step, agent_info = line.strip().split(':')
        step = int(step)
        agent_info = agent_info.split(';')
        movements[step] = {int(agent_data.split(',')[0]): (float(agent_data.split(',')[1]), float(agent_data.split(',')[2]))
                           for agent_data in agent_info}

    # Visualize agent movements and deaths
    fig, ax = plt.subplots()
    counter = ax.text(0.02, 0.95, '', transform=ax.transAxes, color='red')

    for step in movements:
        ax.clear()

        # Plot agents
        for agent_id, (x, y) in movements[step].items():
            if agent_id in movements[step]:
                color = 'red' if agent_id <= len(movements[step]) // 2 else 'blue'
                marker = 'X' if agent_id <= len(movements[step]) // 2 else 'o'
                ax.scatter(x, y, c=color, marker=marker)

        # Set plot limits
        ax.set_xlim([0, 200])
        ax.set_ylim([0, 200])

        # Add labels and title
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title(f'Step {step}')

        # Update and display counter
        death_count = death_counts[steps.index(step)] if step in steps else 0
        counter.set_text(f"Deaths: {death_count}")

        # Pause to visualize each step
        plt.pause(0.1)

    # Display the final plot
    plt.show()

if __name__ == "__main__":
    deaths_file = "deaths_team_a_gettysburg.csv", "deaths_team_b_gettysburg.csv"  # Replace with the actual deaths file name
    movements_file = "agent_movements_gettysburg.txt"  # Replace with the actual movements file name
    visualize_movements(deaths_file, movements_file)
