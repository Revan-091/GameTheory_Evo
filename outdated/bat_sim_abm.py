# class, defining agents as abstract data types
class agent:
    # init-method, the constructor method for agents
    def __init__(self,x,y,group):
        self.life = 100 # agent's life score
        self.x = x
        self.y = y
        self.group = group

# creating empty 100 x 100 list using list comprehension in python
battlefield = [[None for i in range(0,100)] for i in range(0,100)]

# define a function for creating agents and assigning them to grid
def agentCreator(size,group,groupList,field,n,m):
    # loop through entire group, i.e. in this case 1000 units
    for j in range(0,size):
        # select random available location 
        while True:
            # random x coordinate
            x = random.choice(range(0,n))
            # random y coordinate
            y = random.choice(range(0,m))
            # check if spot is available; if not then re-iterate 
            if field[x][y] == None:
                field[x][y] = agent(x=x,y=y,group=group)
                # append agent object reference to group list
                groupList.append(field[x][y])
                # exit while loop; spot on field is taken
                break
# import pyplot and colors from matplotlib
from matplotlib import pyplot, colors
# define function for plotting battlefield (all agents that are still alive)
def plotBattlefield(populationArr, plotTitle):
    # using colors from matplotlib, define a color map
    colormap = colors.ListedColormap(["lightgrey","green","blue"])
    # define figure size using pyplot
    pyplot.figure(figsize = (12,12))
    # using pyplot add a title
    pyplot.title(plotTitle, fontsize = 24)
    # using pyplot add x and y labels
    pyplot.xlabel("x coordinates", fontsize = 20)
    pyplot.ylabel("y coordinates", fontsize = 20)
    # adjust x and y axis ticks, using pyplot
    pyplot.xticks(fontsize = 16)
    pyplot.yticks(fontsize = 16)
    # use .imshow() method from pyplot to visualize agent locations
    pyplot.imshow(X = populationArr, cmap = colormap)

# this function maps a battlefield grid to a numeric grid with 1 for agents of type A, 2 for type B and 0 for no agent
def mapBattlefield(battlefieldArr):
    #.imshow() needs a matrix with float elements;
    populationArr = [[0.0 for i in range(0,100)] for i in range(0,100)]
    # if agent is of type A, put a 1.0, if of type B, pyt a 2.0
    for i in range(1,100):
        for j in range(1,100):
            if battlefieldArr[i][j] == None: # empty
                pass # leave 0.0 in population cell
            elif battlefieldArr[i][j].group == "A": # group A agents
                populationArr[i][j] = 1.0 # 1.0 means "A"
            else: # group B agents
                populationArr[i][j] = 2.0 # 2.0 means "B"
    # return mapped values
    return(populationArr)

# function for creating an initial battlefield grid
def initBattlefield(populationSizeA,populationSizeB,battlefieldArr):
    # initializing new empty battlefield grid, using list comprehension in Python
    battlefieldArr = [[None for i in range(0,100)] for i in range(0,100)]
    # create empty list for containing agent references in future, type A & B
    agents_A = []
    agents_B = []
    # assigning random spots to agents of group A and B; 
    import random
    agentCreator(size = populationSizeA,
                    group = "A",
                    groupList = agents_A,
                    field = battlefieldArr,
                    n = 100,
                    m = 100)
    agentCreator(size = populationSizeB,
                    group = "B",
                    groupList = agents_B,
                    field = battlefieldArr,
                    n = 100,
                    m = 100)
    # return populated battlefield grid
    return(battlefieldArr)

# executing above function for a population size of 1000 for both groups
battlefield = initBattlefield(populationSizeA=1000,populationSizeB=1000,battlefieldArr = battlefield)

# plot battlefield status
plotBattlefield(populationArr = mapBattlefield(battlefield), 
                    plotTitle = "battlefield
