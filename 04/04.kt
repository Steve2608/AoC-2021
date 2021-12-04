import java.io.File

private class Bingo(board: List<String>) {
	val numbers: Array<IntArray>
	val marked: Array<BooleanArray>
	val calledNumbers: MutableList<Int> = mutableListOf(-1)

	init {
		fun getLine(board: List<String>, line: Int) =
			board[line].split("\\s+".toRegex()).filter { it.isNotBlank() }.map { it.toInt() }.toIntArray()
		numbers = Array(board.size) { i -> getLine(board, i) }
		marked = Array(board.size) { i -> getLine(board, i).map { false }.toBooleanArray() }
	}

	override fun toString(): String {
		val n = numbers.joinToString(separator = "\n") {
			it.joinToString(separator = " ") { num ->
				String.format(
					"%02d",
					num
				)
			}
		}
		val b =
			marked.joinToString(separator = "\n") { it.joinToString(separator = " ") { mark -> if (mark) "XX" else "__" } }
		return n + "\n" + b
	}

	fun callNumber(number: Int) {
		numbers.forEachIndexed { i, a ->
			val index = a.indexOf(number)
			if (index >= 0) marked[i][index] = true
		}
		calledNumbers.add(number)
	}

	val hasWinner: Boolean
		get() {
			for (booleans in marked) {
				if (booleans.all { it }) return true
			}
			for (i in 0..marked.lastIndex) {
				var column = true
				for (booleans in marked) {
					if (!booleans[i]) {
						column = false
						break
					}
				}
				if (column) return true
			}
			return false
		}

	val winningScore: Int
		get() {
			var sum = 0
			for (i in 0..numbers.lastIndex) {
				for (j in 0..numbers[i].lastIndex) {
					if (!marked[i][j]) sum += numbers[i][j]
				}
			}
			return sum * calledNumbers.last()
		}

}

private fun part1(filename: String): Int {
	val (numbers, boards) = File(filename).readData()
	numbers.forEach {
		for (board in boards) {
			board.callNumber(it)
			if (board.hasWinner) return board.winningScore
		}
	}
	return -1
}

private fun part2(filename: String): Int {
	val (numbers, boards) = File(filename).readData()
	var prev = boards.toMutableList()
	var curr = mutableListOf<Bingo>()

	numbers.forEach {
		prev.forEachIndexed { i, board ->
			board.callNumber(it)
			if (board.hasWinner) {
				if (prev.size == 1) return board.winningScore
			} else {
				curr.add(board)
			}
		}
		prev = curr
		curr = mutableListOf()
	}
	return -1
}

private fun File.readData(): Pair<IntArray, MutableList<Bingo>> {
	val lines = this.readLines().filter { it.isNotBlank() }
	val numbers = lines[0].split(",").map { it.toInt() }.toIntArray()

	val games: MutableList<Bingo> = mutableListOf()
	for (i in 1..lines.lastIndex step 5) {
		val board = lines.subList(i, i + 5)
		games.add(Bingo(board))
	}

	return Pair(numbers, games)
}

fun main() {
	assert(4512 == part1("example.txt")) { "Expected 188 * 24 = 4512" }
	assert(1924 == part2("example.txt")) { "Expected 148 * 13 = 1924" }

	println(part1("input.txt"))
	println(part2("input.txt"))
}