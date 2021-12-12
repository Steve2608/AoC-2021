from collections import defaultdict, Counter
from functools import partial
from typing import Iterator


def count_distinct_paths(lines: list[tuple[str, str]], small_cave_max_visit: int) -> int:
    def small_cave_count(path: list[str]) -> int:
        c = Counter(filter(str.islower, path))
        return sum(c.values()) - len(c)

    def construct_path(path: list[str]) -> Iterator[list[str]]:
        for option in connections[path[-1]]:
            if option == 'end':
                yield path[:] + ['end']
            elif option != 'start':
                attempt = path[:] + [option]
                if option.isupper() or small_cave_count(attempt) < small_cave_max_visit:
                    yield from construct_path(attempt)


    connections = defaultdict(set)
    for a, b in lines:
        connections[a].add(b)
        connections[b].add(a)

    return sum(map(bool, construct_path(['start'])))


part1 = partial(count_distinct_paths, small_cave_max_visit=1)
part2 = partial(count_distinct_paths, small_cave_max_visit=2)


if __name__ == '__main__':
    if __debug__:
        with open('example.txt') as in_file:
            lines = list(map(lambda line: tuple(line.rstrip().split('-')), in_file))
        assert part1(lines) == 10, f'{part1(lines)=} != 10'
        assert part2(lines) == 36, f'{part2(lines)=} != 36'

    with open('input.txt') as in_file:
        lines = list(map(lambda line: tuple(line.rstrip().split('-')), in_file))
    print(part1(lines))
    print(part2(lines))