import numpy as np
import cv2

notwalkable = []

class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.G = 0
        self.F = 0
        self.H = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(map, start, end):
    global notwalkable
    start_node = Node(None, start)
    start_node.G = start_node.H = start_node.F = 0
    end_node = Node(None, end)
    end_node.G = end_node.H = end_node.F = 0
    open_list =[]
    closed_list = []
    open_list.append(start_node)

    while len(open_list) > 0:
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list): #this means you compare current node with open_list node.
            if item.F < current_node.F: #if openlist item's F is small than current node's F, you changes openlist.
                current_node = item
                current_index = index
        open_list.pop(current_index)
        closed_list.append(current_node)

        if current_node == end_node:
            path=[]
            print (path)
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        children =[]
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: #adjacent node
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1] ) #Get adjacent node position
            if node_position[0] > (len(map) - 1) or node_position[0] < 0 or node_position[1] > (len(map[len(map)-1]) -1) or node_position[1] < 0: #check if node is out side end of map. like [0,-1]. there is no -1 array number.
                continue
            if map[node_position[1]][node_position[0]] != 0: # Make sure walkable terrain
                #print("node_p1:",node_position[1])
                #print("node_p0:",node_position[0])
                print("not walkable place = ", (node_position[0], node_position[1]))
                notgood = [node_position[0],node_position[1]]
                notwalkable.append(notgood)
                continue
            new_node = Node(current_node, node_position)  # this means, make current node as a parent and adjacent position as node position.
            children.append(new_node) #put this new nodes in the children !!!! By for moon, this will put all the adjacent node in the children

        for child in children: #if child in children has already in the closed_list
            for closed_child in closed_list:
                if child == closed_child: #so it child is already in the closed_list, ignore them
                    continue
            child.G = current_node.G + 1 #adjacent node(child) get +1 from current node's G score
            child.H = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.F = child.G + child.H
            #print("child.g", child.G, "child.h", child.H, "child.f", child.F)
            for open_node in open_list:
                if child == open_node and child.G > open_node.G:
                    continue
            open_list.append(child)
