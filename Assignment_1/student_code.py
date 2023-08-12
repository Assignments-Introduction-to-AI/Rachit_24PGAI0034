from expand import expand
from dfs import dfs_search
from bfs import bfs_search
from a_star import astar

def a_star_search (dis_map, time_map, start, end):
	path = astar(time_map, dis_map, start, end)
	return path

def depth_first_search(time_map, start, end):
	path = dfs_search(time_map, start, end)
	return path

def breadth_first_search(time_map, start, end):
	path = bfs_search(time_map, start, end)
	return path