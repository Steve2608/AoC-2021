import java.io.File

private class Ocean(val diagonals: Boolean) {
	data class Point(val x: Int, val y: Int)

	private val counts: MutableMap<Point, Int> = HashMap()

	val mostDangerous: Int
		get() = counts.values.filter { it >= 2 }.size

	private fun addPoint(point: Point) {
		counts[point] = counts.getOrElse(point) { 0 } + 1
	}

	fun expandPoints(start: Point, end: Point) {
		val smaller: Point
		val bigger: Point
		if (start.x == end.x && start.y != end.y) {
			if (end.y < start.y) {
				smaller = end
				bigger = start
			} else {
				smaller = start
				bigger = end
			}
			for (i in smaller.y..bigger.y) {
				addPoint(Point(start.x, i))
			}
		} else if (start.x != end.x && start.y == end.y) {
			if (end.x < start.x) {
				smaller = end
				bigger = start
			} else {
				smaller = start
				bigger = end
			}
			for (i in smaller.x..bigger.x) {
				addPoint(Point(i, start.y))
			}
		} else if (diagonals) {
			if (end.x < start.x) {
				smaller = end
				bigger = start
			} else {
				smaller = start
				bigger = end
			}
			// main diagonal
			if (smaller.y < bigger.y) {
				for (i in 0..bigger.x - smaller.x) {
					addPoint(Point(smaller.x + i, smaller.y + i))
				}
			}
			// second diagonal
			else {
				for (i in 0..bigger.x - smaller.x) {
					addPoint(Point(smaller.x + i, smaller.y - i))
				}
			}
		}
	}
}

private fun oceanSpots(data: List<Pair<Ocean.Point, Ocean.Point>>, diagonals: Boolean): Int {
	val ocean = Ocean(diagonals)
	for ((start, end) in data) {
		ocean.expandPoints(start, end)
	}
	return ocean.mostDangerous
}

private fun part1(data: List<Pair<Ocean.Point, Ocean.Point>>): Int = oceanSpots(data, diagonals = false)
private fun part2(data: List<Pair<Ocean.Point, Ocean.Point>>): Int = oceanSpots(data, diagonals = true)

private fun File.readData(): List<Pair<Ocean.Point, Ocean.Point>> = this
	.readLines()
	.filter { it.isNotBlank() }
	.map { it.split("\\s+->\\s+".toRegex()) }
	.map {
		val point1 = it[0].split(",")
		val point2 = it[1].split(",")
		return@map Pair(
			point1.map { i -> i.toInt() },
			point2.map { i -> i.toInt() }
		)
	}
	.map {
		Pair(
			Ocean.Point(it.first[0], it.first[1]),
			Ocean.Point(it.second[0], it.second[1])
		)
	}

fun main() {
	val example = File("example.txt").readData()
	assert(5 == part1(example)) { "expected 5 dangerous areas" }
	assert(12 == part2(example)) { "expected 12 dangerous areas" }

	val data = File("input.txt").readData()
	println(part1(data))
	println(part2(data))
}

