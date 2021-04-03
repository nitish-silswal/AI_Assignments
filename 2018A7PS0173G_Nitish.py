#!/usr/bin/env python3
from Agent import * # See the Agent.py file
from pysat.solvers import Glucose3
import copy
from math import sqrt

# Knowledge Base : Currently Contains
#7xy -> mine in x,y
#8xy -> safe x,y -> no mines in surrounding cells of x,y
#1xy -> 1 mine percieved around x,y
#4xy -> more than 1 mines percieved around x,y
# First and Last cells are safe so they do not contain mines in them ( Mines in a cell x,y are signified by 7xy )

class Knowledge_Base(object):
    """docstring for Knowledge_Base"""
    def __init__(self):
        super(Knowledge_Base, self).__init__()
        self.kb = list()
        self.kb.extend([[-744],[-711],[-723, -113, -712,] , [-732, -133, -734] , [-813, -712] , [-822, -732] , [713, 733, 722, -423] , [-734, -133, -723] , [-724, -134, -733] , [712, 714, -413] , [712, 723, 721, -422] , [-723, -133, -743]  ])
        self.kb.extend([[842, 741, 732, 743] , [811] , [813, 712, 723, 714] , [712, 732, 723, -422] , [-712, -122, -732] , [723, 714, -413] , [-722, -123, -724] , [723, 732, 721, -422] , [824, 714, 723, 734] , [-732, -131, -721]  ])
        self.kb.extend([[833, 732, 734, 723, 743] , [722, -123, 713, 724, 733] , [431, -741, -721, -732] , [-714, -113, -712] , [433, -723, -743, -732, -734] , [711, -112, 722, 713] , [732, -133, 723, 734, 743] , [712, 723, -413] , [744, 724, -434] , [741, 721, -431] ])
        self.kb.extend([[712, -411] , [-734, -124, -723] , [-823, -724] , [-744, -134, -733] , [721, -131, 741, 732] , [742, -441] , [-714, -124, -723] , [-812, -711] , [422, -712, -732, -721, -723] , [734, -444]  ])
        self.kb.extend([[-821, -711] , [722, 711, -421] , [423, -713, -733, -722, -724] , [711, 713, -412] , [-731, -121, -711] , [812, 711, 722, 713] , [-743, -142, -741] , [713, -111, 724] , [722, 742, 733, -432]  ])
        self.kb.extend([[-713, -112, -711] , [742, 733, -443] , [444, -734, -743] , [713, 724, 722, -423] , [-721, -122, -712] , [-834, -724] , [-832, -731] , [-823, -722] , [-724, -123, -733] , [-821, -722]  ])
        self.kb.extend([[-722, -123, -713] , [-734, -133, -743] , [-733, -132, -742] , [-823, -713] , [-731, -121, -722] , [-842, -741] , [-843, -744] , [-813, -723] , [-733, -132, -722] , [-723, -113, -714]  ])
        self.kb.extend([[723, 734, -424] , [-732, -133, -723] , [411, -712, -721] , [-823, -733] , [-731, -132, -733] , [743, -444] , [-834, -744] , [-832, -722] , [712, -122, 722, 723, 732] , [731, -132, 722, 733, 742]  ])
        self.kb.extend([[712, 732, 721, -422] , [-833, -743] , [-722, -112, -711] , [-732, -142, -741] , [734, 743, 732, -433] , [723, 743, 734, -433] , [-824, -714] , [-824, -734] , [-834, -733] , [741, 743, -442] ])
        self.kb.extend([[-731, -132, -722] , [-841, -731] , [-842, -743] , [724, 733, 722, -423] , [-734, -124, -714] , [-722, -123, -733] , [741, 732, -431] , [-822, -712] , [723, 743, 732, -433] , [731, 722, -421] , ])
        self.kb.extend([[-721, -111, -712] , [443, -742, -744, -733] , [434, -733, -724, -744] , [-722, -132, -742] , [-822, -723] , [743, -111, 734] , [722, 733, 731, -432] , [742, -143, 733, 744] , [-741, -131, -721] , [-844, -734] ])
        self.kb.extend([[711,712, -111, 721] , [744,-734, 711,-144, -743] , [711,712,744, -113, 723, 714] , [744,-732, 711,-133, -743] , [742, 744, -443,711] , [814, 713, 724,711] , [-831, -721,744] , [-822, -721,711] , [841, 742, 731,744] , [823, 722, 724, 713, 733] ])
        self.kb.extend([[711,-812, -722] , [-814, -713,711] , [-724, -123, -713] , [413, 711, -712, -714, -723] , [711, -121, 731, 722] , [-824, -723, 711] , [-833, -734, 711] , [713, 733, 724, -423] , [733, -134, 744, 724] , [-721, -122, -723]  ])
        self.kb.extend([[744,-723, -122, -732] , [744,711,-841, -742] , [-814, -724,711] , [821, 722, 731, 711] , [744,-722, -121, -711] , [742, -111, 731] , [831, 732, 721, 741] , [822, 721, 723, 712, 732] , [-732, -142, -743] , [733, 744, -443] , ])
        self.kb.extend([[711, 722, -412] , [-833, -732, 711] , [-721, -122, -732, 711] , [-832, -733,711] , [711,733, 742, 731, -432] , [-821, -731] , [442, -741, -743, -732] , [722, 713, -412] , [721, -411] , [-731, -132, -742]  ])
        self.kb.extend([[-842, -732] , [731, 711, -421] , [811, 712, 721] , [843, 733, 744, 742] , [412, -711, -713, -722] , [832, 722, 742, 731, 733] , [723, 714, -424] , [421, -731, -711, -722] , [-843, -733] , [734, 714, -424]  ])
        self.kb.extend([[-812, -713] , [723, 734, 732, -433] , [-733, -143, -744] , [-722, -112, -713] , [-713, -123, -733] , [-744, -134, -724] , [424, -723, -714, -734] , [844] , [-811, -721] , [723, -124, 734, 714] , ])
        self.kb.extend([[-731, -141, -742] , [432, -722, -742, -731, -733] , [733, 724, -434] , [-832, -742] , [414, -713, -724] , [-733, -143, -742] , [441, -731, -742] , [722, 742, 731, -432] , [-724, -114, -713] , [844, 734, 743]  ])
        self.kb.extend([[732, 721, -431] , [-844, -743] , [733, 744, -434] , [-833, -723] , [-831, -741] , [724, -414] , [-723, -122, -712] , [741, 732, -442] , [-744, -143, -742]  ])
        self.kb.extend([[711,732, 743, -442] , [-741, -131, 711 , -732] , [-831, -732, 711] , [711,-843, -742] , [-811, -712, 711] , [-813, -714] , [711, 741, -142, 732, 743] , [834, 724, 733, 744] , [713, -414 , 711] , [731, -441]  ])




#### You can change the main function as you wish. Run this program to see the output. Also see Agent.py code.
###############################################################################################################

def fill_grid(N):
    grid = list()
    for i in range(0,N):
        for j in range(0,N):
            grid.append([i+1,j+1])
    return grid


def is_safe(row,column,g):
    temp = (7*100+(10*row)+column) + 10*10;
    temp -= 100;
    lst = list()
    lst.append(temp)
    return (not g.solve(assumptions = lst))

###############################################################################################################

def sortfunc(val):
    return (8-(val[0]+val[1]) + 100  - 10*10);

###############################################################################################################
def findallsafe(grid, safe, g):
    for el in grid:
        if el in safe:
            continue        
        if el not in safe and is_safe(el[0], el[1],g):
            safe.append(el)
###############################################################################################################

class Node:
    def __init__(self,pos):   
        self.parent = None     
        self.best_fitt = int(1e3)
        self.pos = pos
        self.f = 0
  
    def __eq__(self, other):
        if(self.pos != other.pos) : return False
        return True

    def generatesuccessors_ASTAR(self , source , g):
        possible_direction = [[0,1],[0,-1],[-1,0],[1,0]]
        x,y = self.pos
        successors = list()
        for i in range(4):
            newX = x + possible_direction[i][0]
            newY = y + possible_direction[i][1]
            if newX >= 1 and newX <= 4 and newY >= 1 and newY <= 4 and is_safe( newX , newY,g):
                newNode = Node([newX , newY])
                comp = (source[1] + source[0]) * 100
                comp /= 100;
                newNode.f = 100 + (abs(newNode.pos[1] + newNode.pos[0] - comp) + (8 - (newNode.pos[0] + newNode.pos[1]))) * sqrt(100);
                newNode.f -= 100 ; newNode.f /= 10;
                successors.append(newNode)
        return successors

    # Generate all possible safe successors of a given Node
    def generatesuccessors_IDDFS(self, g):
        possible_direction = [[0,1],[0,-1],[-1,0],[1,0]]
        x,y = self.pos
        successors = list()
        for i in range(4):
            newX = x + possible_direction[i][0]
            newY = y + possible_direction[i][1]
            if newX >= 1 and newX <= 4 and newY >= 1 and newY <= 4 and is_safe(newX , newY, g):
                successors.append(Node([newX , newY]))
        return successors
  
###############################################################################################################

def findleastf(openlist, current):
    comp  = (current[1] + current[0]) * 100 ; comp /= 100;
    min_el = openlist[0] 
    min_val = abs(comp - (min_el.pos[0] + min_el.pos[1]))
    for elem in openlist:
        if abs(comp  - (elem.pos[0] + elem.pos[1])) < min_val :
            min_el = elem
        else:
            elem =  None
    return min_el

###############################################################################################################

def pathify(elem, current):
    lst = list()
    while True:
        if elem.pos == current : break
        par = elem.parent
        lst.insert(0, elem)
        elem = par
    return lst      
###############################################################################################################

def reversepathify(el, goal):
    lst = list()
    lst.append(el) ; lst.pop();
    while True:
        if el.parent.pos in goal : break;
        par = el.parent
        lst.append(par)
        el = par
    el = el.parent
    if el.parent is None or el.parent is not None:
        lst.append(el)
    return lst

#############################################################################################################
def is_prime(n):
    i = 2
    while i*i <= n:
        if n % i == 0:
            return False
        i += 1
    return True
###############################################################################################################

def get_destination(openlist , current , goal):
    if len(goal) > 1:
        for el in goal:
            temp = Node(el)
            temp.f = 0
            openlist.append(temp)
            return Node(current)

    temp = Node(current)
    temp.f = 0
    openlist.append(temp)
    return Node(goal[0])

###############################################################################################################
def astar(current, goal, allowed, g):
    openlist = list()
    closedlist = list()

    destination = get_destination(openlist , current , goal)

    while(len(openlist))>0:
        foundflag=False
        q = findleastf(openlist, current)
        openlist.remove(q)
        successors = list()
        successors.append([1]); successors.pop();
        successors.extend(q.generatesuccessors_ASTAR(current , g));
        for elem in successors:
            skipflag = False
            elem.parent=q
            if is_prime(2) and elem == destination:
                foundflag=True
                break
            for check in openlist:
                if check == elem and elem.f >= check.f:
                    skipflag = True
                    break
        
            if skipflag == True:
                continue
            for check in closedlist:
                if check == elem and elem.f >= check.f:
                    skipflag = True
                    break
            if is_prime(5) and skipflag == True:
                continue
            openlist.append(elem)
        if is_prime(5) and foundflag == True:
            if len(goal) != 1:
                return reversepathify(elem , goal)
            else:
                return pathify(elem , current)
        closedlist.append(elem); closedlist.pop();
        closedlist.append(q)

    return None


##############################################################################################################

def print_path(finalpath):
    for i in range(len(finalpath)-1):
        print(finalpath[i] , end = " => ")
    print(finalpath[len(finalpath)-1])

###############################################################################################################

# Iterative Deepening DFS
def iterative_deeping_search(tempagent, initial, goal, max_depth , g):
    current_depth = 0
    while True:
        if current_depth > max_depth:
            return False
        path = list()
        path.append(initial.pos)
        can_reach = dfs(tempagent , initial , goal , current_depth , path , g)
        if can_reach:
            return True
        current_depth += 1

def dfs(tempagent, node, goal, depth, path , g):
    if not (depth > 0) :
        return False
    if node == goal:
        print()
        print("Optimal/Shortest possible path (taking RISKS and without showing backtracked nodes) .... using IDDFS :- ")
        print_path(path);
        return True

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

    # Generate successors to the node and dfs on those with depth-1
    for el in node.generatesuccessors_IDDFS(g):
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
        if dfs(newagent, el, goal, depth-1, newpath , g) == True:
            return True
    return False


##############################################################################################################    

if __name__=='__main__':

    g = Glucose3()
    ag = Agent()
    KB = Knowledge_Base()
    for el in KB.kb:
        g.add_clause(el)

    grid = fill_grid(4)

    #####################################
    finalpath = list();
    safe = list();
    unvisited = list()
    for el in grid:
        unvisited.append(el)

    apply_IDDFS = False
    found_answer_using_ASTAR = False
    while(True):
        x,y = ag.FindCurrentLocation()  
        #unvisited.remove([x,y])
        could_remove = False
        for el in unvisited:
            if el == [x,y]:
                unvisited.remove([x,y])
                could_remove = True
                break

        if could_remove == False:
            print("Agent stuck ...... no further moves allowable due to non-involvement of risk")
            apply_IDDFS = True
            break



        if(x == 4 and y == 4):
            finalpath.append([4,4])
            found_answer_using_ASTAR = True
            break
        # If percept return =0, then the cells adjacent have to be clear. So current cell is safe: add 6xy to KB
        extra_info = -1
        if(ag.PerceiveCurrentLocation()=='=0'):
            temp = 8 * 100 + (10*x) + y - 10*10 + 100
        # If percept return >=1, then mines are present: add -6xy to KB 
        else:
            temp = -1*(8*100 + (10*x) + y) + 100 - 10*10
            # If percept returns =1, then only one of the adjacent cells has a mine: add 1xy to KB alongside -6xy
            if(ag.PerceiveCurrentLocation()=='=1'):
                extra_info = 1*100 + (10*x) + y + 100 - 10*10
            else:
                extra_info = 4*100 + (10*x) + y - 100 + 10*10
        
        lstt = [temp]
        g.add_clause(lstt);
        lstt.pop();
        if extra_info != -1:
         lstt.append(extra_info)
         g.add_clause(lstt)

        #####################################
        findallsafe(grid, safe, g)
        path = astar([x,y],[[4,4]],safe, g)
        # If no path to the goal exists, find a path to the closest unvisited node that is safe.
        if path is None:
            goals = list();
            for el in unvisited:
                goals.append(el)
                if el not in safe:
                    goals.pop()
            path = astar([x,y],goals,safe, g)     


        while True :
            if path is None or len(path) == 0:
                break
            x,y = ag.FindCurrentLocation()
            el = path.pop(0)
            finalpath.append([x,y])
            
            dy = el.pos[1] - y + 10; dy -= 10;
            dx = el.pos[0] - x + 20; dx -= 20;             

            if dx == -1 and dy == 0 :
                ag.TakeAction("Left")
            elif dx == 1 and dy == 0 :
                ag.TakeAction('Right')
            elif dx == 0 and dy == 1 :
                ag.TakeAction('Up')
            elif dx == 0 and dy == -1 :
                ag.TakeAction('Down')


    # IDDFS solution
    ag2 = Agent()
    tempagent = copy.deepcopy(ag2)
    g2 = Glucose3()
    for el in KB.kb:
        g2.add_clause(el)
    final_value = iterative_deeping_search(tempagent, Node([1,1]), Node([4,4]), 10 , g2)

    if found_answer_using_ASTAR == True:
        print()
        print("Path followed by the agent (all visited tiles and taking NO RISK) .... using A-STAR :-")
        print_path(finalpath);
    else:
        print("Unable to reach [4,4] without taking RISKS")

    if final_value == False:
        print("FAILURE .... can't reach [4,4]")

        
