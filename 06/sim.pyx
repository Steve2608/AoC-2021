cpdef simulate_pop(pop: list[int], unsigned int days, unsigned int offset):
    cdef int i = offset % 9
    for day in range(days):
        pop[(i + 7) % 9] += pop[i]
        i = (i + 1) % 9
    return sum(pop)
