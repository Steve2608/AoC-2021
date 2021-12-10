def part1(lines: list[tuple[str, str]]) -> int:
    return sum(
        sum(len(elem) in {2, 3, 4, 7} for elem in out_val.split(' '))
        for _, out_val in lines
    )


def part2(lines: list[tuple[str, str]]) -> int:
    class iSet(set):
        def unset(self):
            if len(self) == 1:
                return next(iter(self))
            else:
                raise ValueError(self)

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

    def deduce_by_length(numbers: list[str]) -> dict[str, iSet[str]]:
        random = {k: iSet('abcdefg') for k in 'abcdefg'}

        for num in map(set, numbers):
            if len(num) == 2:
                # 1
                random['c'].intersection_update(num)
                random['f'].intersection_update(num)
            elif len(num) == 3:
                # 7
                random['a'].intersection_update(num)
                random['c'].intersection_update(num)
                random['f'].intersection_update(num)
            elif len(num) == 4:
                # 4
                random['b'].intersection_update(num)
                random['c'].intersection_update(num)
                random['d'].intersection_update(num)
                random['f'].intersection_update(num)
            elif len(num) == 5:
                # 2, 3, 5
                random['a'].intersection_update(num)
                random['d'].intersection_update(num)
                random['g'].intersection_update(num)
            elif len(num) == 6:
                # 0, 6, 9
                random['a'].intersection_update(num)
                random['b'].intersection_update(num)
                random['f'].intersection_update(num)
                random['g'].intersection_update(num)
            else:
                # '8'
                pass
        return random

    def deduction(assignment: dict[str, iSet[str]]) -> dict[str, iSet[str]]:
        changed = True
        while changed:
            changed = False
            for k, v in assignment.items():
                if len(v) == 1:
                    v_ = v.unset()
                    for k_ in filter(lambda k_: k_ != k, assignment):
                        if v_ in assignment[k_]:
                            changed = True
                            assignment[k_].discard(v_)
        return assignment

    def inverse_assignment(assignment: dict[str, iSet[str]]) -> dict[str, str]:
        return {v.unset(): k for k, v in assignment.items()}

    def construct_number(assignment: dict[str, str], numbers: list[str]) -> int:
        sum_ = 0
        for num in numbers:
            n = tuple(map(lambda char: assignment[char], num))
            sum_ = sum_ * 10 + light_to_number[tuple(sorted(n))]
        return sum_

    def get_number(line: tuple[str, str]) -> int:
        in_val, out_val = line
        in_vals = in_val.split(' ')
        out_vals = out_val.split(' ')

        assignment = deduce_by_length(numbers=in_vals + out_vals)
        assignment = deduction(assignment)
        inv_assignment = inverse_assignment(assignment)
        return construct_number(inv_assignment, out_vals)

    return sum(map(get_number, lines))


if __name__ == '__main__':
    if __debug__:
        with open('example.txt') as in_file:
            lines = list(map(lambda line: tuple(line.rstrip().split(' | ')), in_file.readlines()))
        assert part1(lines) == 26, f'{part1(lines)=} != 26'
        assert part2(lines) == 61229, f'{part2(lines)=} != 61229'

    with open('input.txt') as in_file:
        lines = list(map(lambda line: tuple(line.rstrip().split(' | ')), in_file.readlines()))
    print(part1(lines))
    print(part2(lines))
