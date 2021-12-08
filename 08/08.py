def part1(lines: list[tuple[str, str]]) -> int:
    count = 0
    for _, out_val in lines:
        for elem in out_val.strip().split(' '):
            # 1, 7, 4, 8
            if len(elem) in {2, 3, 4, 7}:
                count += 1

    return count


def part2(lines: list[tuple[str, str]]) -> int:
    light_to_number = {
        tuple('abcefg'): 0,
        tuple('cf'): 1,
        tuple('acdeg'): 2,
        tuple('acdfg'): 3,
        tuple('bcdf'): 4,
        tuple('abdfg'): 5,
        tuple('abdefg'): 6,
        tuple('acf'): 7,
        tuple('abcdefg'): 8,
        tuple('abcdfg'): 9,
    }

    def deduce_by_length():
        random = {
            'a': set('abcdefg'),
            'b': set('abcdefg'),
            'c': set('abcdefg'),
            'd': set('abcdefg'),
            'e': set('abcdefg'),
            'f': set('abcdefg'),
            'g': set('abcdefg'),
        }

        for num in numbers:
            num_set = set(num)
            if len(num) == 2:
                # 1
                random['c'].intersection_update(num_set)
                random['f'].intersection_update(num_set)
            elif len(num) == 3:
                # 7
                random['a'].intersection_update(num_set)
                random['c'].intersection_update(num_set)
                random['f'].intersection_update(num_set)
            elif len(num) == 4:
                # 4
                random['b'].intersection_update(num_set)
                random['c'].intersection_update(num_set)
                random['d'].intersection_update(num_set)
                random['f'].intersection_update(num_set)
            elif len(num) == 5:
                # 2, 3, 5
                random['a'].intersection_update(num_set)
                random['d'].intersection_update(num_set)
                random['g'].intersection_update(num_set)
            elif len(num) == 6:
                # 0, 6, 9
                random['a'].intersection_update(num_set)
                random['b'].intersection_update(num_set)
                random['f'].intersection_update(num_set) # <-- da hatte ich 'e' und nichts ist gegangen.
                random['g'].intersection_update(num_set)
            else:
                # '8'
                pass
        return random

    def deduction(assignment: dict[str, set[str]]):
        old = -1
        while old != sum(map(len, assignment.values())):
            old = sum(map(len, assignment.values()))
            assignment_reduced = assignment.copy()
            for k, v in assignment_reduced.items():
                if len(v) == 1:
                    v_ = next(iter(v))
                    for k_ in assignment:
                        if k != k_:
                            assignment[k_].discard(v_)
            assignment = assignment_reduced
        return assignment

    def inverse_assignment(assignment: dict[str, set[str]]) -> dict[str, str]:
        return {next(iter(v)): k for k, v in assignment.items()}

    def construct_number(assignment: dict[str, str], numbers: list[str]):
        sum_ = 0
        for num in numbers:
            n = tuple()
            for char in num:
                n += tuple(assignment[char])
            sum_ = sum_ * 10 + light_to_number[tuple(sorted(n))]
        return sum_

    total = 0
    for in_val, out_val in lines:
        in_vals = in_val.strip().split(' ')
        out_vals = out_val.strip().split(' ')
        numbers = in_vals + out_vals

        assignment = deduce_by_length()
        assignment = deduction(assignment)
        inv_assignment = inverse_assignment(assignment)
        total += construct_number(inv_assignment, out_vals)
    return total


if __name__ == '__main__':
    with open('example.txt') as in_file:
        lines = list(map(lambda line: tuple(line.strip().split(' | ')), in_file.readlines()))

    assert part1(lines) == 26, f'{part1(lines)=} != 26'
    assert part2(lines) == 61229, f'{part2(lines)=} != 61229'

    with open('input.txt') as in_file:
        lines = list(map(lambda line: tuple(line.split('|')), in_file.readlines()))

    print(part1(lines))
    print(part2(lines))
