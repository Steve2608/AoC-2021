from collections import Counter, deque

if __name__ == '__main__':
    def simulate_pop(pop: deque, days: int):
        pop_iter = pop.copy()
        for day in range(days):
            p = pop_iter.popleft()
            pop_iter[6] += p
            pop_iter.append(p)
        return sum(pop_iter), pop_iter

    with open('input.txt') as in_file:
        counts = Counter(map(int, in_file.read().strip().split(',')))

    pop0 = deque([counts[i] for i in range(9)])
    part1, pop80 = simulate_pop(pop0, days=80)
    part2, pop256 = simulate_pop(pop80, days=256 - 80)
    print(part1, part2, sep='\n')
