# Functions to apply
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


# def astar(time_map)
