import heapq
from typing import Tuple, Dict, List, Optional


def heuristic_cost_estimate(
        start: Tuple[int, int], goal: Tuple[int, int], size: Tuple[int, int]
) -> int:
    """
    Estimate the cost from the start point to the goal point using the Manhattan distance.

    Args:
        start (Tuple[int, int]): The starting point coordinates.
        goal (Tuple[int, int]): The goal point coordinates.
        size (Tuple[int, int]): The size of the grid.

    Returns:
        int: The estimated cost from start to goal.
    """
    dx = abs(goal[0] - start[0])
    dy = abs(goal[1] - start[1])
    return min(dx, size[0] - dx) + min(dy, size[1] - dy)


def reconstruct_path(
        came_from: Dict[Tuple[int, int], Tuple[int, int]], current: Tuple[int, int]
) -> List[Tuple[int, int]]:
    """
    Reconstructs the path from the start to the current node.

    Args:
        came_from (Dict[Tuple[int, int], Tuple[int, int]]): A dictionary storing parent-child relationships.
        current (Tuple[int, int]): The current node.

    Returns:
        List[Tuple[int, int]]: The path from the start to the current node.
    """
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path[::-1]


def find_path_with_omission(
        size: Tuple[int, int],
        start: Tuple[int, int],
        goal: Tuple[int, int],
        omitted_points: List[Tuple[int, int]],
) -> Optional[List[Tuple[int, int]]]:
    """
    Finds a path from start to goal while avoiding specified omitted points.

    Args:
        size (Tuple[int, int]): The size of the grid.
        start (Tuple[int, int]): The starting point coordinates.
        goal (Tuple[int, int]): The goal point coordinates.
        omitted_points (List[Tuple[int, int]]): A list of coordinates to be omitted during pathfinding.

    Returns:
        List[Tuple[int, int]]: The path from start to goal avoiding omitted points.
    """
    open_set = [(0, start)]
    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from, current)

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            neighbor = ((current[0] + dx) % size[0], (current[1] + dy) % size[1])
            if neighbor in omitted_points:
                continue

            tentative_g_score = g_score[current] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic_cost_estimate(
                    neighbor, goal, size
                )
                heapq.heappush(open_set, (f_score, neighbor))

    return []
