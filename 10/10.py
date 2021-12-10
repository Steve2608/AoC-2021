chunk_open = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}

# hackerman
class stack(list):
    def push(self, elem):
        self.append(elem)


def _corrupt_points(line: str) -> int:
    points = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137
    }

    s = stack()
    for char in line:
        if char in chunk_open:
            s.push(char)
        else:
            assert char in chunk_open.values(), f'Invalid character encountered {char}'

            if chunk_open[s.pop()] != char:
                return points[char]
    return 0


def _missing_points(line: str) -> int:
    points = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4
    }

    s = stack()
    for char in line:
        if char in chunk_open:
            s.push(char)
        else:
            s.pop()
    assert s, 'stack must not be empty'

    score = 0
    while s:
        score = score * 5 + points[chunk_open[s.pop()]]
    return score


def part1(lines: list[str]) -> int:
    return sum(map(_corrupt_points, lines))


def part2(lines: list[str]) -> int:
    scores = sorted(_missing_points(line) for line in filter(lambda l: _corrupt_points(l) == 0, lines))
    return scores[len(scores) // 2]


if __name__ == '__main__':
    if __debug__:
        with open('example.txt') as in_file:
            data = in_file.read().splitlines()
        assert part1(data) == 26397, f'{part1(data)=} != 26'
        assert part2(data) == 288957, f'{part1(data)=} != 26'

    with open('input.txt') as in_file:
        data = in_file.read().splitlines()
    print(part1(data))
    print(part2(data))
