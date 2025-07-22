import queue as q
import math as m
import random
import networkx as nx

graph_data = [
    [0, 1100, 0, 0, 1800, 0, 0],
    [1100, 0, 1500, 0, 0, 0, 0],
    [0, 1500, 0, 900, 700, 0, 1700],
    [0, 0, 900, 0, 400, 1000, 0],
    [1800, 0, 700, 400, 0, 0, 0],
    [0, 0, 0, 1000, 0, 0, 200],
    [0, 0, 1700, 0, 0, 200, 0]
]

h = {
    (0,1):80, (1,0):80, (0,4):60, (4,0):60,
    (1,2):50, (2,1):50,
    (2,3):45, (3,2):45, (2,4):30, (4,2):30,
    (2,6):90, (6,2):90,
    (3,4):15, (4,3):15, (3,5):50, (5,3):50,
    (5,6):10, (6,5):10
}

coordinates = [[0,0], [8,6], [22,7], [15,12], [15.7,8.5], [6,8], [5,7]]

def speedlimit(a, b):
    return h[(a, b)]

def time_weighted_graph():
    G = nx.Graph()
    for i in range(len(graph_data)):
        for j in range(len(graph_data)):
            if graph_data[i][j] != 0:
                weight = graph_data[i][j] / speedlimit(i, j)
                G.add_edge(i, j, weight=weight)
    return G

def add_traffic(G):
    for u, v in G.edges():
        delay = random.randint(0, 100)
        G[u][v]['weight'] += delay

def heuristic(state, goal):
    x1, y1 = coordinates[state]
    x2, y2 = coordinates[goal]
    return m.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def run_astar(G, start, goal):
    open = q.PriorityQueue()
    closed = q.PriorityQueue()
    visited = [start]
    cl = []
    open.put([heuristic(start, goal), 0.0, start, None])

    def updateopen(next, fn, cost, parent):
        temp = open.get()
        if temp[2] == next:
            if cost < temp[1]:
                open.put([fn, cost, next, parent])
            else:
                open.put(temp)
            return
        updateopen(next, fn, cost, parent)
        open.put(temp)

    def updateclosed(next, fn, cost, parent):
        templist = []
        while True:
            temp = closed.get()
            if temp[2] == next:
                if cost < temp[1]:
                    closed.put([fn, cost, next, parent])
                    for i in templist:
                        closed.put(i)
                    propogateimprovement(next, cost)
                else:
                    closed.put(temp)
                    for i in templist:
                        closed.put(i)
                break
            else:
                templist.append(temp)

    def propogateimprovement(next, cost):
        for each in G.neighbors(next):
            costnew = cost + G[next][each]['weight']
            fnnew = costnew + heuristic(each, goal)
            if each in visited:
                updateopen(each, fnnew, costnew, next)
            if each in cl:
                updateclosed(each, fnnew, costnew, next)

    def resultlist(closed):
        result = []
        while not closed.empty():
            result.append(closed.get())
        return result, result[-1][1]

    def pathgenerator(closed, parent, goal):
        if parent is None:
            return [goal]
        for i in closed:
            if i[2] == goal:
                for j in closed:
                    if j[2] == i[3]:
                        return pathgenerator(closed, j[3], j[2]) + [i[2]]

    while not open.empty():
        temp = open.get()
        visited.remove(temp[2])
        closed.put(temp)
        cl.append(temp[2])
        if temp[2] == goal:
            result, total_time = resultlist(closed)
            path = pathgenerator(result, temp[3], goal)
            return total_time, path
        else:
            for next in G.neighbors(temp[2]):
                cost = temp[1] + G[temp[2]][next]['weight']
                fn = cost + heuristic(next, goal)
                if next not in visited and next not in cl:
                    open.put([fn, cost, next, temp[2]])
                    visited.append(next)
                elif next in visited:
                    updateopen(next, fn, cost, temp[2])
                elif next in cl:
                    updateclosed(next, fn, cost, temp[2])

    return None, []
