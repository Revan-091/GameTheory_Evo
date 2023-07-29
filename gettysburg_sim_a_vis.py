import matplotlib.pyplot as plt


def visualize_deaths(deaths_file):
    # Read the deaths file
    with open(deaths_file, 'r') as file:
        lines = file.readlines()

    # Extract step and death counts from the deaths file
    steps = [int(line.strip().split(',')[0]) for line in lines]
    death_counts = [int(line.strip().split(',')[1]) for line in lines]

    # Visualize deaths
    fig, ax = plt.subplots()
    counter = ax.text(0.02, 0.95, '', transform=ax.transAxes, color='red')

    for step, death_count in zip(steps, death_counts):
        ax.clear()

        # Set plot limits
        ax.set_xlim([0, 200])
        ax.set_ylim([0, 200])

        # Add labels and title
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title(f'Step {step}')

        # Update and display counter
        counter.set_text(f"Deaths: {death_count}")

        # Pause to visualize each step
        plt.pause(0.1)

    # Display the final plot
    plt.show()

def visualize_movements(movements_file):
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

    # Visualize agent movements
    fig, ax = plt.subplots()

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

        # Pause to visualize each step
        plt.pause(0.1)

    # Display the final plot
    plt.show()

if __name__ == "__main__":
    deaths_file_team_a = "deaths_team_a_gettysburg.csv"  
    deaths_file_team_b = "deaths_team_b_gettysburg.csv"  
    movements_file = "agent_movements_gettysburg.txt"    

    # Visualize deaths for team A
    visualize_deaths(deaths_file_team_a)

    # Visualize deaths for team B
    visualize_deaths(deaths_file_team_b)

    # Visualize movements
    visualize_movements(movements_file)
