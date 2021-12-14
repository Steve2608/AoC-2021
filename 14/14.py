from collections import defaultdict
from functools import partial


def polymer_chain(polymer: str, rules: dict[str, str], steps: int) -> int:
    def highest_minus_lowest(counts: dict[str, int]):
        letter_counts = defaultdict(int)
        for k, v in counts.items():
            for letter in k:
                letter_counts[letter] += v
        
        # special handling of first / last letter
        letter_counts[polymer[0]] += 1
        letter_counts[polymer[-1]] += 1
        
        highest = max(letter_counts.values())
        lowest = min(letter_counts.values())
        return (highest - lowest) // 2

    # initial counts
    counts = defaultdict(int)
    for a, b in zip(polymer[:-1], polymer[1:]):
        counts[a + b] += 1

    # polymerization
    for _ in range(steps):
        c = defaultdict(int)
        for k, v in counts.items():
            x, z = k
            y = rules[k]

            c[x + y] += v
            c[y + z] += v
        counts = c

    return highest_minus_lowest(counts)


part1 = partial(polymer_chain, steps=10)
part2 = partial(polymer_chain, steps=40)


if __name__ == '__main__':
    if __debug__:
        with open('example.txt') as in_file:
            polymer, rules = in_file.read().split('\n\n')
            rules = dict(tuple(rule.split(' -> ')) for rule in rules.splitlines())
        assert part1(polymer, rules) == 1588, f'{part1(polymer, rules)=} != 1588'
        assert part2(polymer, rules) == 2188189693529, f'{part2(polymer, rules)=} != 2188189693529'

    with open('input.txt') as in_file:
        polymer, rules = in_file.read().split('\n\n')
        rules = dict(rule.split(' -> ') for rule in rules.splitlines())
    print(part1(polymer, rules))
    print(part2(polymer, rules))