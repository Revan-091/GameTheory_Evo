# Background

This battle simulation program is a Python-based application that simulates a battlefield scenario of the battle of Gettysburg, a very important battle of the American Civil War, between two teams, Team A and Team B, which depict the Confederate troops (Team A), and the Union troops (Team B), which were present at the time, consisting of soldiers and cavalry. The program uses game theory concepts to guide agents' decision-making, allowing for strategic combat interactions. The simulation takes place on a 2D grid, where agents have attributes like health, attack range, and attack strength. The program visualizes the battlefield in real-time using Matplotlib and records agent deaths in each step, facilitating analysis and comparison of team performance. It serves as a valuable tool for studying AI strategies, agent interactions, and game theory applications in complex scenarios. For the sake of the program, the number of agents is proportional to the actual number of soldiers who were active in the battle.

# Running the code

Before running the actual code:

Make sure to have these two libraries installed, as they are pivotal for the program.

```
pip install matplotlib
```
This library will plot the simulation.

```
pip install nashpy
```
This library facilittes the use of game theory on the simulation.


To run the code:

```
python3 gettysburg_gt_sim_a.py --num_soldiers ### --num_cavalry ###
```


What this code does is create two sides to the battle, team A (which will depict the union), and the opponent team (which will depict the Confederation).
For both teams, it creates also two types of units (agents): Infantry, which have lower health, but higher range; and cavalry, which have a higher health and strength of attack, but lower attack range. The two teams will then choose the best strategy from a dictionary which will contain them, based on the best_response_index to the other agent's action. Deaths will be removed from the battlefield grid and numerated, as well as the movements made by the agents as to visualize them in the next program.

The user will input the command above, and instead of hashtags, the user will be able to manipulate the number of infantry and cavalry available, as to conduct soft research into what would have happened if the numbers of the battle changed.

In order to create a more historical accurate representation, the number of troops would go like this
```
python3 gettysburg_gt_sim_a.py --num_soldiers 1155 --num_cavalry 495
```
But of course, the user can play with the numbers as they wish.


### The folder named "outdated"...
Serves the purpose of storing my past programs for this project.