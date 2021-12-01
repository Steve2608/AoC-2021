import java.io.File

fun File.readData() = this.readLines().map { s -> Integer.parseInt(s) }.toIntArray()

fun nIncrease(data: IntArray): Int = nIncrease(data, window_size = 1)

fun nIncrease(data: IntArray, window_size: Int = 3): Int {
	var nIncrease = 0

	var prev = data.slice(0 until window_size).sum()
	for (i in window_size..data.lastIndex) {
		val cur = prev - data[i - window_size] + data[i]
		if (cur > prev) nIncrease++
		prev = cur
	}

	return nIncrease
}

fun main() {
	val example: IntArray = File("example.txt").readData()
	assert(7 == nIncrease(example)) { "Expected 7 increases" }
	assert(5 == nIncrease(example, window_size = 3)) { "Expected 5 increases" }

	val data: IntArray = File("input.txt").readData()
	println(nIncrease(data))
	println(nIncrease(data, window_size = 3))
}
