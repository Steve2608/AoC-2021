cpdef simulate_pop(pop: list[int], int days, int i):
    for day in range(days):
        pop[(i + 7) % 9] += pop[i]
        i = (i + 1) % 9
    return sum(pop)