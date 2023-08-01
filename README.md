# Background
...
# Running the code

To run the code:

```
python3 gettysburg_gt_sim_a.py --num_infantry ### --num_cavalry ###
```


What this code does is create two sides to the battle, team A (which will depict the union), and the opponent team (which will depict the Confederation).
For both teams, it creates also two types of units (agents): Infantry, which have lower health, but higher range; and cavalry, which have a higher health and strength of attack, but lower attack range. The two teams will then choose the best strategy from a dictionary which will contain them, based on the best_response_index to the other agent's action. Deaths will be removed from the battlefield grid and numerated, as well as the movements made by the agents as to visualize them in the next program.

The user will input the command above, and instead of hashtags, the user will be able to manipulate the number of infantry and cavalry available, as to conduct soft research into what would have happened if the numbers of the battle changed.


To visualize it:

```
python3 gettysburg_sim_a_vis.py
```

What this program does is it reads the information stored in the documents pertaining to the deaths of both teams, as well as the movements of each team per step taken in the battle, and will accordingly plot their movements and deaths in the battlefield grid, to create a more user friendly output of the battle, which the user could then compare to the actual result of the battle.

### The folder named "outdated"...
Serves the purpose of storing my past programs in case I were to go back and look at them.