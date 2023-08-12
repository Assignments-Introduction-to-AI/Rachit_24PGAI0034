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
