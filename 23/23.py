from functools import partial


def parse_board(filename: str):
    with open(filename) as in_file:
        board = ['.'] * 11
        next(in_file)
        next(in_file)
        first = next(in_file)
        second = next(in_file)

        for i in (3, 5, 7, 9):
            board[i - 1] = first[i] + second[i]
    return board


def dijkstra(board: list[str]):
    def key(board: list[str]):
        return tuple(board)

    def is_room(board: list[str], i: int):
        return len(board[i]) > 1

    def can_move(board: list[str], src: int, dest: int):
        a = min(src, dest)
        b = max(src, dest)
        return not any(i != src and i not in goal_spaces and board[i] != '.' for i in range(a, b+1))

    def goal_or_empty(board: list[str], amphipod: str, dest: int):
        room = board[dest]
        n_amphipods = room.count(amphipod)
        n_empty = room.count('.')
        return len(room) == n_amphipods + n_empty

    def get_amphipod(room: str):
        # get first amphipod for room / hallway 
        for c in room:
            if c != '.':
                return c

    def to_room(letter: str, room: str) -> tuple[str, int]:
        n_empty = room.count('.')

        assert n_empty != 0
        room = list(room)
        room[n_empty - 1] = letter
        return ''.join(room), n_empty

    def possible_moves(board: list[str], src: int):
        amphipod = board[src]
        
        # if on hallway
        if src not in goal_spaces:
            g_pos = goals[amphipod]

            # if we can move to a room immediately do that
            if can_move(board, src, g_pos) and goal_or_empty(board, amphipod, g_pos):
                return [goals[amphipod]]

            # otherwise do not move twice on hallway
            return []

        # in room
        amphipod = get_amphipod(amphipod)

        # room is already complete
        if src == goals[amphipod] and goal_or_empty(board, amphipod, src):
            return []

        possible = []
        for dest in range(len(board)):
            if dest == src or (dest in goal_spaces and goals[amphipod] != dest):
                continue
            if goals[amphipod] == dest:
                if not goal_or_empty(board, amphipod, dest):
                    continue
            if can_move(board, src, dest):
                possible.append(dest)
        return possible

    def move(board: list[str], pos: int, dest: int):
        # copy board
        new_board = board[:]
        dist = 0
        
        amphipod = get_amphipod(board[pos])
        if is_room(board, pos):
            room_old = board[pos]
            room_new = ''

            found = False
            # move out first amphipod from room
            for c in room_old:
                if c == '.':
                    dist += 1
                    room_new += c
                elif not found:
                    room_new += '.'
                    dist += 1
                    found = True
                else:
                    room_new += c
            new_board[pos] = room_new
        else:
            new_board[pos] = '.'
        
        dist += abs(pos - dest)

        if is_room(board, dest):
            new_board[dest], move_cost = to_room(amphipod, board[dest])
            dist += move_cost
            return new_board, dist * costs[amphipod]
        else:
            new_board[dest] = amphipod
            return new_board, dist * costs[amphipod]

    goals = {
        'A': 2,
        'B': 4,
        'C': 6,
        'D': 8,
    }

    goal_spaces = set(goals.values())

    costs = {
        'A': 1,
        'B': 10,
        'C': 100,
        'D': 1000,
    }

    states = {key(board): 0}
    queue = [board]

    while queue:
        board = queue.pop()
        for pos, state in enumerate(board):
            if get_amphipod(state):
                dests = possible_moves(board, pos)

                for dest in dests:
                    new_board, move_cost = move(board, pos, dest)
                    new_cost = states[key(board)] + move_cost

                    # maximum upper bound if state not yet encountered
                    cost = states.get(new_key := key(new_board), float('Inf'))
                    if new_cost < cost:
                        states[new_key] = new_cost
                        queue.append(new_board)

    return states


def get_costs(board: list[str], target: tuple[str]):
    nodes = dijkstra(board)
    return nodes.get(target, -1)


part1 = partial(get_costs, target=('.', '.', 'A'*2, '.', 'B'*2, '.', 'C'*2, '.', 'D'*2, '.', '.'))
part2 = partial(get_costs, target=('.', '.', 'A'*4, '.', 'B'*4, '.', 'C'*4, '.', 'D'*4, '.', '.'))


if __name__ == '__main__':
    def extension():
        yield 'DD'
        yield 'CB'
        yield 'BA'
        yield 'AC'

    if __debug__:
        board = parse_board('example.txt')
            
        assert (p1 := part1(board)) == 12521, f'{p1} != 12521'

        ext = extension()
        board = [(b if len(b) == 1 else b[0] + next(ext) + b[-1]) for b in board]
        assert (p2 := part2(board)) == 44169, f'{p2} != 44169'

    board = parse_board('input.txt')
    print(part1(board))
    
    ext = extension()
    board = [(b if len(b) == 1 else b[0] + next(ext) + b[-1]) for b in board]
    print(part2(board))