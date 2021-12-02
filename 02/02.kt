import java.io.File
import kotlin.math.abs

private data class Direction(val direction: String, val length: Int) {
	fun toVec2(): Vec2 = when (direction) {
		"forward" -> Vec2(length, 0)
		"down" -> Vec2(0, length)
		"up" -> Vec2(0, -length)
		else -> throw IllegalArgumentException(direction)
	}

	fun toVec3(): Vec3 = when (direction) {
		"forward" -> Vec3(length, 0, 0)
		"down" -> Vec3(0, 0, length)
		"up" -> Vec3(0, 0, -length)
		else -> throw IllegalArgumentException(direction)
	}
}

private data class Vec2(val x: Int, val y: Int) {
	operator fun plus(other: Vec2) = Vec2(x + other.x, y + other.y)
}

private data class Vec3(val x: Int, val y: Int, val aim: Int) {
	operator fun plus(other: Vec3) = Vec3(x + other.x, y + other.x * aim, aim + other.aim)
}

private fun part1(directions: Array<Direction>): Int {
	val pos = directions.map { it.toVec2() }.reduce { acc, vec2 -> acc + vec2 }
	return abs(pos.x) * abs(pos.y)
}

private fun part2(directions: Array<Direction>): Int {
	val pos = directions.map { it.toVec3() }.reduce { acc, vec3 -> acc + vec3 }
	return abs(pos.x) * abs(pos.y)
}

fun main() {
	fun File.readData() = this.readLines().map {
		val split = it.split(" ")
		return@map Direction(direction = split[0], length = split[1].toInt())
	}.toTypedArray()

	val example: Array<Direction> = File("example.txt").readData()
	assert(150 == part1(example)) { "Expected 15 * 10 = 150" }
	assert(900 == part2(example)) { "Expected 15 * 60 = 900" }

	val data: Array<Direction> = File("input.txt").readData()
	println(part1(data))
	println(part2(data))
}
