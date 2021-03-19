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
KB = [
#7xy -> mine in x,y
#8xy -> safe x,y -> no mines in surrounding cells of x,y
#1xy -> 1 mine percieved around x,y
#4xy -> more than 1 mines percieved around x,y
    [844],
# Safety of a cell implies there is no mine in adjacent cells. Safe Cells are signified as 8xy
    [-811, -712], [-811, -721], [811, 712, 721],
    [-844, -734], [-844, -743], [844, 734, 743],
    [-841, -731], [-841, -742], [841, 742, 731],
    [-814, -724], [-814, -713], [814, 713, 724],
    [-813, -712], [-813, -723], [-813, -714], [813, 712, 723, 714],
    [-824, -714], [-824, -723], [-824, -734], [824, 714, 723, 734],
    [-834, -724], [-834, -733], [-834, -744], [834, 724, 733, 744],
    [-821, -711], [-821, -731], [-821, -722], [821, 722, 731, 711],
    [-831, -721], [-831, -741], [-831, -732], [831, 732, 721, 741],
    [-842, -732], [-842, -741], [-842, -743], [842, 741, 732, 743],
    [-843, -744], [-843, -742], [-843, -733], [843, 733, 744, 742],
    [-822, -721], [-822, -723], [-822, -712], [-822, -732], [822, 721, 723, 712, 732],
    [-823, -722], [-823, -724], [-823, -713], [-823, -733], [823, 722, 724, 713, 733],
    [-832, -722], [-832, -742], [-832, -731], [-832, -733], [832, 722, 742, 731, 733],
    [-833, -732], [-833, -734], [-833, -723], [-833, -743], [833, 732, 734, 723, 743],
    [-812, -711], [-812, -722], [-812, -713], [812, 711, 722, 713],
    
# If percept was one means only one of the adjacent cells can have bomb ( 1 percept is shown as 1xy )
  
    [-721, -111, -712], [712, -111, 721],
    [-724, -114, -713], [713, -111, 724],
    [-731, -141, -742], [742, -111, 731],
    [-734, -144, -743], [743, -111, 734], 
    [-722 , -112 , -711], [-713 , -112 , -711], [- 722 , -112 , -713], [711 , -112 , 722 , 713],
    [-723 , -113 , -712], [-714 , -113 , -712], [- 723 , -113 , -714], [712 , -113 , 723 , 714],
    [-734 , -124 , -723], [-714 , -124 , -723], [- 734 , -124 , -714], [723 , -124 , 734 , 714],
    [-744 , -134 , -733], [-724 , -134 , -733], [- 744 , -134 , -724], [733 , -134 , 744 , 724],
    [-731 , -121 , -711], [-722 , -121 , -711], [- 731 , -121 , -722], [711 , -121 , 731 , 722],
    [-741 , -131 , -721], [-732 , -131 , -721], [- 741 , -131 , -732], [721 , -131 , 741 , 732],
    [-732 , -142 , -741], [-743 , -142 , -741], [- 732 , -142 , -743], [741 , -142 , 732 , 743],
    [-733 , -143 , -742], [-744 , -143 , -742], [- 733 , -143 , -744], [742 , -143 , 733 , 744],
    [-721, -122, -712], [-723 , -122 , -712 ], [- 721 , -122 , -723], [-721 , -122 , -732], [-723 , -122 , -732], [-712 , -122 , -732], [712, -122, 722, 723, 732],
    [-722, -123, -713], [-724 , -123 , -713 ], [- 722 , -123 , -724], [-722 , -123 , -733], [-724 , -123 , -733], [-713 , -123 , -733], [722, -123, 713, 724, 733],
    [-731, -132, -722], [-733 , -132 , -722 ], [- 731 , -132 , -733], [-731 , -132 , -742], [-733 , -132 , -742], [-722 , -132 , -742], [731, -132, 722, 733, 742],
    [-732, -133, -723], [-734 , -133 , -723 ], [- 732 , -133 , -734], [-732 , -133 , -743], [-734 , -133 , -743], [-723 , -133 , -743], [732, -133, 723, 734, 743],
# If percept was more than one means more than one adjacent cells has bomb (shown as 4xy )
    [711, 722, -412], [722, 713, -412], [711, 713, -412],
    [712, 723, -413], [723, 714, -413], [712, 714, -413], 
    [731, 722, -421], [722, 711, -421], [731, 711, -421], 
    [741, 732, -431], [732, 721, -431], [741, 721, -431], 
    [741, 732, -442], [732, 743, -442], [741, 743, -442], 
    [742, 733, -443], [733, 744, -443], [742, 744, -443],
    [723, 734, -424], [734, 714, -424], [723, 714, -424], 
    [733, 744, -434], [744, 724, -434], [733, 724, -434], 
    [712, 732, 721, -422], [712, 732, 723, -422], [712, 723, 721, -422], [723, 732, 721, -422], 
    [713, 733, 722, -423], [713, 733, 724, -423], [713, 724, 722, -423], [724, 733, 722, -423], 
    [722, 742, 731, -432], [722, 742, 733, -432], [722, 733, 731, -432], [733, 742, 731, -432], 
    [723, 743, 732, -433], [723, 743, 734, -433], [723, 734, 732, -433], [734, 743, 732, -433],
    
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
            if newX >= 1 and newX <= 4 and newY >= 1 and newY <= 4 and is_safe(newX , newY , g):
                successors.append(Node([newX , newY]))
        return successors

###############################################################################################################
# Check safety using satisfiability of there being a bomb in the location - If satisfiable then position unsafe
def is_safe(row , column , g):
    temp = 700+(10*row)+column + 1000;
    temp -= 1000;
    para = list()
    para.append(temp)
    return (not g.solve(assumptions = para))
###############################################################################################################
# Iterative Deepening DFS
def ida(g, tempagent, initial, goal, max_depth):
    for depth in range(0,max_depth+1):
        path = [initial.pos]
        print("depth is " + str(depth))
        if(search(g, tempagent, initial,goal,depth, path)==True):
        	print("Path is : " , path)
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
        temp = 800 + (10*x) + y
    # If percept return >=1, then mines are present: add -8xy to KB 
    else:
        temp = -1*(800 + (10*x) + y)
        # If percept returns =1, then only one of the adjacent cells has a mine: add 1xy to KB alongside -8xy
        if(tempagent.PerceiveCurrentLocation()=='=1'):
            extra_info = 100 + (10*x) + y
        else:
            extra_info = 400 + (10*x) + y
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

        newpath.append(el.pos)
        if search(g, newagent, el, goal, depth-1, newpath):
            return True
    return False

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
    final_value = ida(g, tempagent, Node([1,1]), Node([4,4]), 10);    
    if final_value == False:
    	print("Not possible to reach the destination ")

