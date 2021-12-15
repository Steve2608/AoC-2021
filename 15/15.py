from queue import PriorityQueue
from typing import Iterator


def UCS(grid: list[list[int]], visited: set[tuple[int, int]], queue: PriorityQueue, is_goal: callable) -> int:
    def children(node: tuple[int, int]) -> Iterator[tuple[int, int]]:
        x, y = node
        if x > 0:
            yield x - 1, y
        if x < len(grid) - 1:
            yield x + 1, y
        if y > 0:
            yield x, y - 1
        if y < len(grid[x]) - 1:
            yield x, y + 1

    while not queue.empty():
        cost, parent = queue.get()
        for node in children(parent):
            if node not in visited:
                x, y = node
                if is_goal(node):
                    return cost + grid[x][y]
                else:
                    queue.put((cost + grid[x][y], (x, y)))
                    visited.add((x, y))
    else:
        return -1


def part1(grid: list[list[int]]) -> int:
    visited = {(0, 0)} 
    queue = PriorityQueue()
    queue.put((0, (0, 0)))
    is_goal = lambda node: node[0] == len(grid) - 1 and node[1] == len(grid[-1]) - 1
    return UCS(grid, visited, queue, is_goal)


def part2(grid: list[list[int]]) -> int:
    def expand_grid(grid: list[list[int]], x_times: int, y_times: int):
        def wrap(value: int) -> int:
            if value > 9:
                return value % 9
            return value

        x_grid = [[] for _ in grid]
        for i, line in enumerate(grid):
            for x in range(x_times):
                x_grid[i].extend([wrap(v + x) for v in line])

        xy_grid = []  
        for y in range(y_times):
            for line in x_grid:
                xy_grid.append([wrap(v + y) for v in line])
        
        return xy_grid

    expanded_grid = expand_grid(grid, x_times=5, y_times=5)
    visited = {(0, 0)} 
    queue = PriorityQueue()
    queue.put((0, (0, 0)))
    is_goal = lambda node: node[0] == len(expanded_grid) - 1 and node[1] == len(expanded_grid[-1]) - 1
    return UCS(expanded_grid, visited, queue, is_goal)


if __name__ == '__main__':
    if __debug__:
        with open('example.txt') as in_file:
            grid = [list(map(int, line.strip())) for line in in_file]
        assert part1(grid) == 40, f'{part1(grid)=} != 40'
        assert part2(grid) == 315, f'{part2(grid)=} != 315'
    
    with open('input.txt') as in_file:
        grid = [list(map(int, line.strip())) for line in in_file]
    print(part1(grid))
    print(part2(grid))
