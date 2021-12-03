import java.io.File

private class Diagnostics(val data: Array<String>) {
	val lastIndex: Int
		get() = data[0].lastIndex
	private val andBitMask: Int
		get() = (1 shl (lastIndex + 1)) - 1

	val gamma: Int
		get() {
			val counts = IntArray(data[0].length)
			data.forEach { it.forEachIndexed { i, _ -> counts[i] = countBitPosition(data, i) } }
			return counts.map { it >= data.size / 2 }.joinToString(separator = "") { if (it) "1" else "0" }.toInt(2)
		}
	val epsilon: Int
		get() = (gamma xor Int.MAX_VALUE) and andBitMask

	val oxygen: Int?
		get() {
			var filterData = data.toList()
			for (i in 0..lastIndex) {
				filterData = filterData.filter { it[i] == majorityAtBitPosition(filterData, i) }
				if (filterData.size == 1) {
					return filterData[0].toInt(2)
				}
			}
			return null
		}
	val co2: Int?
		get() {
			var filterData = data.toList()
			for (i in 0..lastIndex) {
				filterData = filterData.filter { it[i] == minorityAtBitPosition(filterData, i) }
				if (filterData.size == 1) {
					return filterData[0].toInt(2)
				}
			}
			return null
		}

	private fun countBitPosition(data: Array<String>, position: Int) = data.sumOf { it[position].toString().toInt() }

	private fun majorityAtBitPosition(data: List<String>, position: Int): Char {
		val counts = data.groupingBy { it[position] }.eachCount()
		val comparator = compareByDescending<Map.Entry<Char, Int>> { it.value }.thenByDescending { it.key }
		return counts.entries.sortedWith(comparator).first().key
	}

	private fun minorityAtBitPosition(data: List<String>, position: Int): Char {
		val counts = data.groupingBy { it[position] }.eachCount()
		val comparator = compareBy<Map.Entry<Char, Int>> { it.value }.thenBy { it.key }
		return counts.entries.sortedWith(comparator).first().key
	}

}

private fun part1(data: Array<String>): Int {
	val diagnostics = Diagnostics(data)
	return diagnostics.gamma * diagnostics.epsilon
}

private fun part2(data: Array<String>): Int {
	val diagnostics = Diagnostics(data)
	return diagnostics.oxygen!! * diagnostics.co2!!
}

fun main() {
	fun File.readData() = this.readLines().toTypedArray()

	val example: Array<String> = File("example.txt").readData()
	assert(198 == part1(example)) { "Expected 22 * 9 = 198 increases" }
	assert(230 == part2(example)) { "Expected 23 * 10 = 230 increases" }

	val data: Array<String> = File("input.txt").readData()
	println(part1(data))
	println(part2(data))
}