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


def dfs_traversal(time_map: dict, current_node: str, visited_nodes: list, end: str, parents_dict: dict, found: bool):
    """
    Function to implement recurrsive dfs traversal.\n
    Args:\n
        time_map: graph dictionary.\n
        current_node:the node being visited.\n
        visited_nodes: list of nodes which has been already visited.\n
        end: end node.\n
    """
    visited_nodes.append(current_node)
    connections = get_connections(time_map, current_node)

    for i in connections:
        if i == end: # This would be the base case for the recurssion algorithm
            visited_nodes.append(i)
            found = True
            break
          
        if i not in visited_nodes:
            parents_dict[i] = connections # Connections in this case are list of node, here we are maintaining a parents_dict,
            # so we can find the most efficient path 
            dfs_traversal(time_map, i, visited_nodes, end, parents_dict)


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

    connections = get_connections(time_map, start) # getting the connections for the starting node
    visited_nodes = []
    visited_nodes.append(start)
    parents_dict = {}
    found = False
    for i in connections:
        if i == end:
            found = True
            visited_nodes.append(i)
            break
        if i not in visited_nodes:
            parents_dict[i] = connections # Connections in this case are list of nodes, here we are maintaining a parents_dict,
            # so we can find the most efficient path
            dfs_traversal(time_map, i, visited_nodes, end, parents_dict, found)


