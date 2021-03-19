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
#7xy -> mine in x,y
#8xy -> safe x,y -> no mines in surrounding cells of x,y
#1xy -> 1 mine percieved around x,y
#4xy -> more than 1 mines percieved around x,y
# First and Last cells are safe so they do not contain mines in them ( Mines in a cell x,y are signified by 7xy )

KB = [

    [-811, -712], [-811, -721], [-822, -732], 
    [-844, -734], [-844, -743], [-823, -733], 
    [-841, -731], [-841, -742], [-832, -733],
    [-814, -724], [-814, -713], [-833, -743], 
    [-812, -711], [-812, -722], [-812, -713], 
    [-813, -712], [-813, -723], [-813, -714], 
    [-824, -714], [-824, -723], [-824, -734], 
    [-834, -724], [-834, -733], [-834, -744], 
    [-821, -711], [-821, -731], [-821, -722], 
    [-831, -721], [-831, -741], [-831, -732], 
    [-842, -732], [-842, -741], [-842, -743], 
    [-843, -744], [-843, -742], [-843, -733], 
    [-822, -721], [-822, -723], [-822, -712], 
    [-823, -722], [-823, -724], [-823, -713], 
    [-832, -722], [-832, -742], [-832, -731],  
    [-833, -732], [-833, -734], [-833, -723], 

    [-724, -114, -713], [713, -111, 724],[-734, -144, -743], [743, -111, 734],
    [-721, -111, -712], [821, 722, 731, 711], [834, 724, 733, 744], [831, 732, 721, 741],
    [-731, -141, -742], [742, -111, 731], [824, 714, 723, 734], [842, 741, 732, 743],
    [812, 711, 722, 713],   [813, 712, 723, 714], [- 723 , -113 , -714], [712 , -113 , 723 , 714],
    [-723 , -113 , -712], [-714 , -113 , -712], [843, 733, 744, 742],[712, -111, 721],
    [-734 , -124 , -723], [-714 , -124 , -723], [- 734 , -124 , -714], [723 , -124 , 734 , 714],
    [-744 , -134 , -733], [-724 , -134 , -733], [- 744 , -134 , -724], [733 , -134 , 744 , 724],
    [-731 , -121 , -711], [-722 , -121 , -711], [- 731 , -121 , -722], [711 , -121 , 731 , 722],
    [-741 , -131 , -721], [-732 , -131 , -721], [- 741 , -131 , -732], [721 , -131 , 741 , 732],
    [-732 , -142 , -741], [-743 , -142 , -741], [- 732 , -142 , -743], [741 , -142 , 732 , 743],
    [-733 , -143 , -742], [-744 , -143 , -742], [-722 , -112 , -711], [-713 , -112 , -711],
    [-721, -122, -712], [-723 , -122 , -712 ], [- 721 , -122 , -723], [-721 , -122 , -732], [-723 , -122 , -732], 
    [-722, -123, -713], [-724 , -123 , -713 ], [- 722 , -123 , -724], [-722 , -123 , -733], [-724 , -123 , -733], 
    [-731, -132, -722], [-733 , -132 , -722 ], [- 731 , -132 , -733], [-731 , -132 , -742], [-733 , -132 , -742], 
    [-732, -133, -723], [-734 , -133 , -723 ], [- 732 , -133 , -734], [-732 , -133 , -743], [-734 , -133 , -743], 
    [- 733 , -143 , -744], [742 , -143 , 733 , 744],[- 722 , -112 , -713], [711 , -112 , 722 , 713], 

    [721, -411], [411, -712, -721], [712, -411], [-712 , -122 , -732], [712, -122, 722, 723, 732],
    [731, -441], [742, -441], [441, -731, -742],[-713 , -123 , -733], [722, -123, 713, 724, 733],
    [713, -414], [414, -713, -724],[724, -414], [-722 , -132 , -742], [731, -132, 722, 733, 742],
    [734, -444], [444, -734, -743],[743, -444], [-723 , -133 , -743], [732, -133, 723, 734, 743],
    [723, 714, -413], [823, 722, 724, 713, 733],[841, 742, 731],[412, -711, -713, -722], [822, 721, 723, 712, 732],[814, 713, 724],
    [712, 723, -413], [712, 714, -413], [413, -712, -714, -723],[722, 713, -412], [711, 722, -412],[711, 713, -412],
    [722, 711, -421], [731, 722, -421], [731, 711, -421], [421, -731, -711, -722], [832, 722, 742, 731, 733],[844, 734, 743],
    [741, 732, -431], [732, 721, -431], [741, 721, -431], [431, -741, -721, -732], [833, 732, 734, 723, 743],[811, 712, 721],
    [741, 732, -442], [732, 743, -442],[722, 742, 731, -432], [722, 742, 733, -432], [741, 743, -442], 
    [742, 733, -443], [733, 744, -443], [742, 744, -443], [443, -742, -744, -733], [-744],
    [723, 734, -424], [734, 714, -424], [723, 714, -424], [424, -723, -714, -734], [811],
    [733, 744, -434], [733, 724, -434], [434, -733, -724, -744],[744, 724, -434], [844],
    [723, 732, 721, -422], [422, -712, -732, -721, -723],[712, 732, 721, -422], [712, 732, 723, -422], [712, 723, 721, -422], 
    [433, -723, -743, -732, -734], [723, 734, 732, -433] , [423, -713, -733, -722, -724],[713, 733, 722, -423], [713, 733, 724, -423], 
    [442, -741, -743, -732], [-711],[733, 742, 731, -432], [432, -722, -742, -731, -733],[722, 733, 731, -432],
    [723, 743, 732, -433], [723, 743, 734, -433],[734, 743, 732, -433], [713, 724, 722, -423], [724, 733, 722, -423], 
]

###############################################################################################################

#Node class : Each position's description in the grid
class Node:
    def __init__(self, pos):
        temp = list()
        temp.append(pos)
        self.path = temp
        self.pos = pos
    def __eq__(self, other):
        if other.pos == self.pos:
            return True
        return False


# Generate all possible safe successors of a given Node
    def generatesuccessors(self, g):
        valid_moves = [[0,1],[0,-1],[-1,0],[1,0]]
        x,y = self.pos
        successors = list()
        for i in range(4):
            newX = x + valid_moves[i][0]
            newY = y + valid_moves[i][1]
            if newX >= 1 and newX <= 4 and newY >= 1 and newY <= 4 and is_safe(newX , newY, g):
                successors.append(Node([newX , newY]))
        return successors

    
###############################################################################################################
# Check safety using satisfiability of there being a bomb in the location - If satisfiable then position unsafe
def is_safe(row , column , g):
    temp = 700+(10*row)+column + 100*100
    temp -= (100*100)
    para = list()
    para.append(temp)
    return (not g.solve(assumptions = para))

###############################################################################################################
# Iterative Deepening DFS
def ida(tempagent, initial, goal, max_depth , g):
    for depth in range(0,max_depth+1 , 1):
        path = list()
        path.append(initial.pos)
        print("current_depth is " + str(depth))
        if(search(tempagent, initial,goal,depth, path,g)==True) :
            return True
    return False

def search(tempagent, node, goal, depth, path , g):
    if not (depth > 0) :
        return False
    if node == goal:
        print("Path: ",path)
        return True
    
    #############################################################################
   
    # Update KB with the current information available step
    x,y = tempagent.FindCurrentLocation();
    for_sure = 0;
    if tempagent.PerceiveCurrentLocation() != "=0":
        for_sure = -1 * (800 + 10*x + y);
        if tempagent.PerceiveCurrentLocation() != "=1":
            extra_info = 4*100 + 10*x  +y ;
        else:
            extra_info = 1*100 + 10*x + y ;
        g.add_clause([extra_info]);
    else:
        for_sure = 800 + 10*x + y;
    g.add_clause([for_sure])


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
        if search(newagent, el, goal, depth-1, newpath , g) == True:
            return True
    return False

###############################################################################################################

if __name__ == "__main__" :
    ag = Agent()
    g = Glucose3()

    # Add Knowledge Base to clauses
    for el in KB:
        g.add_clause(el)
   
    tempagent = copy.deepcopy(ag)
    final_value = ida(tempagent, Node([1,1]), Node([4,4]), 10 , g)
    if final_value == False:
        print("Not possible to reach the destination ")