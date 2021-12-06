import java.io.File

const val resetDays = 6
const val newbornDays = 8

private class Population(data: IntArray) : Iterable<MutableMap.MutableEntry<Int, Long>> {
	constructor() : this(IntArray(0))

	private val populationCount: MutableMap<Int, Long> = HashMap()
	val nFish: Long
		get() = populationCount.values.sum()

	init {
		data.forEach {
			populationCount[it] = populationCount.getOrDefault(it, 0) + 1
		}
	}

	fun addPopulation(age: Int, amount: Long) {
		populationCount[age] = populationCount.getOrDefault(age, 0) + amount
	}

	override fun iterator(): MutableIterator<MutableMap.MutableEntry<Int, Long>> = populationCount.iterator()

}

private fun simulatePopulation(data: IntArray, days: Int): Long {
	var pop = Population(data)

	for (i in 1..days) {
		val popNext = Population()
		for ((key, value) in pop) {
			if (key <= 0) {
				popNext.addPopulation(newbornDays, value)
				popNext.addPopulation(resetDays, value)
			} else {
				popNext.addPopulation(key - 1, value)
			}
		}
		pop = popNext
	}
	return pop.nFish
}

private fun part1(data: IntArray) = simulatePopulation(data, days = 80)
private fun part2(data: IntArray) = simulatePopulation(data, days = 256)

fun main() {
	fun File.readData() = this.readLines()[0].split(",").map { it.toInt() }.toIntArray()

	val example = File("example.txt").readData()
	assert(5934L == part1(example)) { "Expected 5934 fish" }
	assert(26984457539L == part2(example)) { "Expected 26984457539 fish" }

	val data = File("input.txt").readData()
	println(part1(data))
	println(part2(data))
}