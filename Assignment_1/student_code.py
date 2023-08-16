from expand import expand
from queue import PriorityQueue
### Functions to apply
def get_connections(time_map: dict, node: str) -> list:
    """
    Function to get the connection list from the graph dictionary.\n
    Args:\n
        time_map: graph dictionary.\n  
        node: node which we want to get the connections.\n
    Returns:\n
        list containing connections.\n
    """

    connection_dict = time_map[node]
    connections = []
    for key, value in connection_dict.items():
        if value:
            connections.append(key)

    return connections

def astar(time_map: dict, dist_map: dict, start: str, end: str):
    """
    Function that implements the astar algorithm.\n
    Args:\n
        time_map: dict = Dictionary where the heuristic value is defined.\n
        dist_map: dict = Dictionary where the path between two nodes is defined.\n
        start: str = Start node.\n
        end: str = End node.\n
    Returns:\n
        path
    """

    # We are going to use Priority Queue to implement the a star algorithm
    priority_queue = PriorityQueue()
    priority_queue.put((0, start))
    parent = {}
    cost_so_far = {}
    parent[start] = None
    cost_so_far[start] = 0
    found = False
    
    while not priority_queue.empty():
        current = priority_queue.get()[1] # Using the index 1 to get the node name
        if end == current:
            found = True
            break

        connections = get_connections(time_map, current)
        for i in connections:
            new_cost = cost_so_far[current] + time_map[current][i]

            if i not in cost_so_far or new_cost < cost_so_far[i]:
                cost_so_far[i] = new_cost
                priority_order = new_cost + dist_map[i][end]
                priority_queue.put((priority_order,i))
                parent[i] = current


    if found:
        path = []
        node = end
        while node != start:
            path.append(node)
            node = parent[node]

        path.append(start)
        path.reverse()

        return path
    
    else:
        return "Not Found"

def dfs_search(time_map: dict , start: str, end: str)-> list:
    """
    Function to apply depth first search algorithm based on the time_map.\n
    dict.\n
    Args:\n
        time_map: dict = Dictionary containing nodes as keys and values as dict containing connections.\n
        start: str = Start Node.\n
        end: str = End Node.\n
    Returns:\n
        list containing path.\n
    """

    # Implementing iterative dfs search
    stack = []
    stack.insert(0,start)
    visited = [] # maintaing list of visited nodes
    found = False
    parent_dict = {} # here child is key and parent is the values
    
    while len(stack) !=0 :
        # Popping operation
        current_node = stack.pop(0)
        if current_node not in visited:
            if current_node == end:
                found = True
                break
            visited.append(current_node)
            connections = get_connections(time_map, current_node)
            for i in connections:
                if i not in visited:
                    stack.insert(0,i)
                    parent_dict[i] = current_node

    if found:
        # Reconstructing the path
        path = [end]
        current_node = end
        while current_node != start:
            path.insert(0, parent_dict[current_node])
            current_node = parent_dict[current_node]
        return path

    else:
        return visited
    


def backtrack(parent_dict: dict, child_node: str, path_stack = []):
    """
    Function to apply the back track algorithm on the parent_dict.\n
    Args:
        parent_dict: dict = Dictionary containing parent as keys and children as keys.\n
        child_node: dict = child node from we have to extract the parent key.\n 
    """

    found_parent = False
    for key, value in parent_dict.items():
        if child_node in value:
            path_stack.insert(0,child_node)
            child_node = key
            found_parent = True
            break

    if found_parent:
        backtrack(parent_dict, child_node, path_stack)

    else:
        path_stack.insert(0, child_node)
        return

def bfs_search(time_map: dict, start: str, end: str)->list:
    """
    Function to apply depth first search algorithm based on the time_map\n
    dict.\n
    Args:\n
        time_map: dict = Dictionary containing nodes as keys and values as dict containing connections.\n
        start: str = Start Node.\n
        end: str = End Node.\n
    Returns:\n
        list containing path.\n
    """

    # Initialising
    queue = []
    queue.append(start)

    # Visited Nodes
    visited = []
    visited.append(start)
    path = []
    parents = {}
    found = False
    
    while queue:
        s = queue.pop(0)
        if s==end:
            found = True
        path.append(s)
        connections = get_connections(time_map, s)
        parents[s] = []
        
        for i in connections:
            if i not in visited:
                queue.append(i)
                visited.append(i)
                parents[s].append(i)
        

    path_stack = []
    if found:
        backtrack(parents, end, path_stack)

    return path_stack


def a_star_search (dis_map, time_map, start, end):
	path = astar(time_map, dis_map, start, end)
	return path

def depth_first_search(time_map, start, end):
	path = dfs_search(time_map, start, end)
	return path

def breadth_first_search(time_map, start, end):
	path = bfs_search(time_map, start, end)
	return path