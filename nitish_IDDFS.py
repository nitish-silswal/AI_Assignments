# #!/usr/bin/env python3
# from Agent import * # See the Agent.py file
# from pysat.solvers import Glucose3
#!/usr/bin/env python3
from Agent import * # See the Agent.py file
from pysat.solvers import Glucose3
import copy
from copy import deepcopy

#### All your code can go here.
###############################################################################################################


# Knowledge Base : Currently Contains
#9xy -> mine in x,y
#6xy -> safe x,y -> no mines in surrounding cells of x,y
#1xy -> 1 mine percieved around x,y
#5xy -> more than 1 mines percieved around x,y
# First and Last cells are safe so they do not contain mines in them ( Mines in a cell x,y are signified by 7xy )

KB = [
# First and Last cells are safe so they do not contain mines in them ( Mines in a cell x,y are signified by 9xy )
    [-911],
    [-944],
# There always exists a safe path so one of 1,2 and 2,1 has to be safe since otherwise we wouldnt be able to leave 1,1. Similar logic can be applied to 4,4
    [611],
    [644],
# Safety of a cell implies there is no mine in adjacent cells. Safe Cells are signified as 6xy
    [-611, -912], [-611, -921], [611, 912, 921],
    [-644, -934], [-644, -943], [644, 934, 943],
    [-641, -931], [-641, -942], [641, 942, 931],
    [-614, -924], [-614, -913], [614, 913, 924],
    [-612, -911], [-612, -922], [-612, -913], [612, 911, 922, 913],
    [-613, -912], [-613, -923], [-613, -914], [613, 912, 923, 914],
    [-624, -914], [-624, -923], [-624, -934], [624, 914, 923, 934],
    [-634, -924], [-634, -933], [-634, -944], [634, 924, 933, 944],
    [-621, -911], [-621, -931], [-621, -922], [621, 922, 931, 911],
    [-631, -921], [-631, -941], [-631, -932], [631, 932, 921, 941],
    [-642, -932], [-642, -941], [-642, -943], [642, 941, 932, 943],
    [-643, -944], [-643, -942], [-643, -933], [643, 933, 944, 942],
    [-622, -921], [-622, -923], [-622, -912], [-622, -932], [622, 921, 923, 912, 932],
    [-623, -922], [-623, -924], [-623, -913], [-623, -933], [623, 922, 924, 913, 933],
    [-632, -922], [-632, -942], [-632, -931], [-632, -933], [632, 922, 942, 931, 933],
    [-633, -932], [-633, -934], [-633, -923], [-633, -943], [633, 932, 934, 923, 943],
# If percept was one means only one of the adjacent cells can have bomb ( 1 percept is shown as 1xy )
    [-921, -111, -912], [912, -111, 921],
    [-924, -114, -913], [913, -111, 924],
    [-931, -141, -942], [942, -111, 931],
    [-934, -144, -943], [943, -111, 934],
    [-922 , -112 , -911], [-913 , -112 , -911], [- 922 , -112 , -913], [911 , -112 , 922 , 913],
    [-923 , -113 , -912], [-914 , -113 , -912], [- 923 , -113 , -914], [912 , -113 , 923 , 914],
    [-934 , -124 , -923], [-914 , -124 , -923], [- 934 , -124 , -914], [923 , -124 , 934 , 914],
    [-944 , -134 , -933], [-924 , -134 , -933], [- 944 , -134 , -924], [933 , -134 , 944 , 924],
    [-931 , -121 , -911], [-922 , -121 , -911], [- 931 , -121 , -922], [911 , -121 , 931 , 922],
    [-941 , -131 , -921], [-932 , -131 , -921], [- 941 , -131 , -932], [921 , -131 , 941 , 932],
    [-932 , -142 , -941], [-943 , -142 , -941], [- 932 , -142 , -943], [941 , -142 , 932 , 943],
    [-933 , -143 , -942], [-944 , -143 , -942], [- 933 , -143 , -944], [942 , -143 , 933 , 944],
    [-921, -122, -912], [-923 , -122 , -912 ], [- 921 , -122 , -923], [-921 , -122 , -932], [-923 , -122 , -932], [-912 , -122 , -932], [912, -122, 922, 923, 932],
    [-922, -123, -913], [-924 , -123 , -913 ], [- 922 , -123 , -924], [-922 , -123 , -933], [-924 , -123 , -933], [-913 , -123 , -933], [922, -123, 913, 924, 933],
    [-931, -132, -922], [-933 , -132 , -922 ], [- 931 , -132 , -933], [-931 , -132 , -942], [-933 , -132 , -942], [-922 , -132 , -942], [931, -132, 922, 933, 942],
    [-932, -133, -923], [-934 , -133 , -923 ], [- 932 , -133 , -934], [-932 , -133 , -943], [-934 , -133 , -943], [-923 , -133 , -943], [932, -133, 923, 934, 943],
# If percept was more than one means more than one adjacent cells has bomb ( shown as 5xy )
    [921, -511], [912, -511], [511, -912, -921],
    [913, -514], [924, -514], [514, -913, -924],
    [931, -541], [942, -541], [541, -931, -942],
    [934, -544], [943, -544], [544, -934, -943],
    [911, 922, -512], [922, 913, -512], [911, 913, -512], [512, -911, -913, -922],
    [912, 923, -513], [923, 914, -513], [912, 914, -513], [513, -912, -914, -923],
    [931, 922, -521], [922, 911, -521], [931, 911, -521], [521, -931, -911, -922],
    [941, 932, -531], [932, 921, -531], [941, 921, -531], [531, -941, -921, -932],
    [941, 932, -542], [932, 943, -542], [941, 943, -542], [542, -941, -943, -932],
    [942, 933, -543], [933, 944, -543], [942, 944, -543], [543, -942, -944, -933],
    [923, 934, -524], [934, 914, -524], [923, 914, -524], [524, -923, -914, -934],
    [933, 944, -534], [944, 924, -534], [933, 924, -534], [534, -933, -924, -944],
    [912, 932, 921, -522], [912, 932, 923, -522], [912, 923, 921, -522], [923, 932, 921, -522], [522, -912, -932, -921, -923],
    [913, 933, 922, -523], [913, 933, 924, -523], [913, 924, 922, -523], [924, 933, 922, -523], [523, -913, -933, -922, -924],
    [922, 942, 931, -532], [922, 942, 933, -532], [922, 933, 931, -532], [933, 942, 931, -532], [532, -922, -942, -931, -933],
    [923, 943, 932, -533], [923, 943, 934, -533], [923, 934, 932, -533], [934, 943, 932, -533], [533, -923, -943, -932, -934]
]




###############################################################################################################
# Global variable to define all possible movements - Up, Down, Left, and Right respectively.
validmoves = [[0,1],[0,-1],[-1,0],[1,0]]

###############################################################################################################
# Class to define Nodes (positions in the grid)
class Node:
    def __init__(self, pos):
        self.pos = pos
        temp = list()
        temp.append(pos)
        self.path = temp
    def __eq__(self, other):
        return self.pos == other.pos



# Generate all possible safe successors of a given Node
    def generatesuccessors(self, g):
        x,y = self.pos
        successors = list()
        for i in range(4):
            newX = x + validmoves[i][0]
            newY = y + validmoves[i][1]
            if newX >= 1 and newX <= 4 and newY >= 1 and newY <= 4 and is_safe(newX , newY, g):
                successors.append(Node([newX , newY]))
        return successors

    
###############################################################################################################
# Check safety using satisfiability of there being a bomb in the location - If satisfiable then position unsafe
def is_safe(row , column , g):
    temp = 900+(10*row)+column + 100*100
    temp -= (100*100)
    para = list()
    para.append(temp)
    return (not g.solve(assumptions = para))

###############################################################################################################
# Iterative Deepening DFS
def ida(g, tempagent, initial, goal, max_depth):
    for depth in range(0,max_depth+1):
        path = [initial.pos]
        print("depth is " + str(depth))
        if(search(g, tempagent, initial,goal,depth, path)==True) :
            return True
    return False

def search(g, tempagent, node, goal, depth, path):
    if node==goal:
        print("Path: ",path)
        return True
    if depth<=0:
        return False
    #############################################################################
    #Updating the knowledge base step (with info gained)
    x,y = tempagent.FindCurrentLocation()
    # If percept return =0, then the cells adjacent have to be clear. So current cell is safe: add 8xy to KB
    if(tempagent.PerceiveCurrentLocation()=='=0'):
        temp = 600 + (10*x) + y
    # If percept return >=1, then mines are present: add -8xy to KB 
    else:
        temp = -1*(600 + (10*x) + y)
        # If percept returns =1, then only one of the adjacent cells has a mine: add 1xy to KB alongside -8xy
        if(tempagent.PerceiveCurrentLocation()=='=1'):
            extra_info = 100 + (10*x) + y
        else:
            extra_info = 500 + (10*x) + y
        g.add_clause([extra_info])
    g.add_clause([temp])

    #############################################################################
   # Generate successors to the node and search on those with depth-1
    for el in node.generatesuccessors(g):
        newagent = copy.deepcopy(tempagent)
        newpath = copy.deepcopy(path)
        dx = el.pos[0] - x; 
        dy = el.pos[1] - y;

        if dx == -1 and dy == 0 :
            newagent.TakeAction("Left")
        elif dx == 1 and dy == 0 :
            newagent.TakeAction('Right')
        elif dx == 0 and dy == 1 :
            newagent.TakeAction('Up')
        elif dx == 0 and dy == -1 :
            newagent.TakeAction('Down')
        else:
            continue


        newpath.append(el.pos)
        if search(g, newagent, el, goal, depth-1, newpath) == True:
            return True
    return False

    # for elem in node.generatesuccessors(g):
    #     newagent = copy.deepcopy(tempagent)
    #     newpath = copy.deepcopy(path)
    #     v=[elem.pos[0]-x, elem.pos[1]-y]
    #     index = validmoves.index(v)
    #     # newpath = copy.deepcopy(path)
    #     if index==0:
    #         newagent.TakeAction('Up')
    #     elif index==1:
    #         newagent.TakeAction('Down')
    #     elif index==2:
    #         newagent.TakeAction('Left')
    #     elif index==3:
    #         newagent.TakeAction('Right')

    #     newpath.append(elem.pos)
    #     if search(g, newagent, elem, goal, depth-1, newpath):
    #         return True
    # return False

###############################################################################################################

if __name__ == "__main__" :
    ag = Agent()
    g = Glucose3()
    #####################################
    # Add Knowledge Base to clauses
    for el in KB:
        g.add_clause(el)
    #####################################
    tempagent = copy.deepcopy(ag)
    final_value = ida(g, tempagent, Node([1,1]), Node([4,4]), 10)
    if final_value == False:
        print("Not possible to reach the destination ")