# Functions to apply bfs algorithm
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




time_map1 = {
    'Campus':{ 'Campus':None, 'Whole_Food':1, 'Beach':1, 'Cinema':None, 'Lighthouse':1, 'Ryan_Field':None, 'YWCA':None },
    'Whole_Food':{ 'Campus':1, 'Whole_Food':None, 'Beach':1, 'Cinema':1, 'Lighthouse':None, 'Ryan_Field':None, 'YWCA':None },
    'Beach':{ 'Campus':1, 'Whole_Food':1, 'Beach':None, 'Cinema':None, 'Lighthouse':None, 'Ryan_Field':None, 'YWCA':None },
    'Cinema':{ 'Campus':None, 'Whole_Food':1, 'Beach':None, 'Cinema':None, 'Lighthouse':None, 'Ryan_Field':None, 'YWCA':1 },
    'Lighthouse':{ 'Campus':1, 'Whole_Food':None, 'Beach':None, 'Cinema':None, 'Lighthouse':None, 'Ryan_Field':1, 'YWCA':None },
    'Ryan_Field':{ 'Campus':None, 'Whole_Food':None, 'Beach':None, 'Cinema':None, 'Lighthouse':1, 'Ryan_Field':None, 'YWCA':1 },
    'YWCA':{ 'Campus':None, 'Whole_Food':None, 'Beach':None, 'Cinema':1, 'Lighthouse':None, 'Ryan_Field':1, 'YWCA':None }
}

path = bfs_search(time_map1, start='Campus', end='Ryan_Field')        

    
