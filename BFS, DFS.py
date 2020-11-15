import ast
import numpy as np

def parse_tuple(string):
    try:
        s = ast.literal_eval(str(string))
        if type(s) == tuple:
            return s
        return
    except:
        return

input_data = input("Does input file exist?(Y/N) : ")

if input_data == "Y":
    file_name = input("Enter file name :")
    location = input("Enter file location :")
    txt = location+"/"+file_name+".txt"
    info = open(txt, 'r')
    line_list = []
    while True:
        line = info.readline()
        line_list.append(line)
        if not line: break
    
    info.close()

    row_col = line_list[1].replace('\n',"").split(' ')
    m = int(row_col[0])  #number of row
    n = int(row_col[1])  #number of column
    start = parse_tuple(line_list[2].replace('\n',"").split(' ')[0])
    goal = parse_tuple(line_list[3].replace('\n',"").split(' ')[0])
    obstacle_num = len(line_list) - 8
    obstacle_list = []
    for i in range(obstacle_num):
        obstacle = parse_tuple(line_list[6+i].replace('\n',"").split(' ')[0])
        obstacle_list.append(obstacle)
    maze = np.zeros((m,n))  
    for obs_pos in obstacle_list:
        maze[obs_pos] = int(1)
    maze = maze.tolist()    

#print(line_list)
#print(start)
#print(goal)
#print(obstacle_list)
#print(maze)              

def DeleteObs(value, obstacle_list):
    for i in value:
        for j in obstacle_list:
            if i == j:
                value.remove(i)
    return value

def GenerateNode(maze):
    row = len(maze)
    col = len(maze[0])
    graph = {}
    for i in range(0, row):
        for j in range(0, col):
            graph[(i,j)] = [(i-1,j), (i+1,j), (i,j-1), (i,j+1)]
    for key in list(graph.keys()):      #list로 변환 후 제거
        if key in obstacle_list:
            del graph[key]
    
    for value in graph.values():
        for i in value:
            if i[0] < 0 or i[0] > row-1:
                value.remove(i)
        for i in value:
            if i[1] < 0 or i[1] > col-1:
                value.remove(i)
                
    for value in graph.values():
        for i in value:
            i = DeleteObs(value, obstacle_list)
    
    expandablenode = graph
    return expandablenode

expandablenode = GenerateNode(maze)


def BFS(expandablenode, start, goal):
    visited = []
    queue = []
    
    queue.append(start)
    while len(queue) != 0:
        if queue[0] == start:
            path = [queue.pop(0)]
        else:
            path = queue.pop(0)
            
        front = path[-1]
        if front == goal:
            return path, len(path), visited
        elif front not in visited:
            for adjacentnode in expandablenode[front]:
                newpath = list(path)
                newpath.append(adjacentnode)
                queue.append(newpath)                   # Keep tracks every path
            visited.append(front)
        #print(path)                                  ## To check how does it tracks down the path

BFS_route, BFS_length, BFS_explored = BFS(expandablenode, start, goal)
print("Route to the goal node :", BFS_route)
print("Total distance :", BFS_length)
print("Explored Nodes :", BFS_explored)


def DFS(expandablenode, start, goal):
    visited = []
    stack =[]
    stack.append(start)
    
    while len(stack) != 0:
        if stack[-1] == start:
            path = [stack.pop(-1)]
        else:
            path = stack.pop(-1)
            
        front = path[-1]
        if front == goal:
            return path, len(path), visited
        elif front not in visited:
            for adjacentnode in expandablenode[front]:
                newpath = list(path)
                newpath.append(adjacentnode)
                stack.append(newpath)
            visited.append(front)
            
DFS_route, DFS_length, DFS_explored = DFS(expandablenode, start, goal)
print("Route to the goal node :", DFS_route)
print("Total distance :", DFS_length)
print("Explored Nodes :", DFS_explored)
