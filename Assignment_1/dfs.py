# Functions to apply dfs aglorithm
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


        