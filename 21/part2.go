package main

import (
	"fmt"
	"os"
	"strconv"
)

const board_size = 10
const win = 21

var dieScoreCombinations map[int]int = map[int]int{3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}

func quantumDieGame(currentPos, otherPos, currentPoints, otherPoints int) []int {
	// if someone won, we're done with this reality
	if currentPoints > 20 { return []int{1, 0} }
	if otherPoints > 20 { return []int{0, 1} }

	results := []int{0, 0}

	// play the rest of the game for all possible next rolls
	for roll, combinations := range dieScoreCombinations {
		// play the next roll
		newPos := mod1(currentPos + roll, 10)
		newPoints := currentPoints + newPos

		// play the rest of the rolls, alternating the current player
		wins := quantumDieGame(otherPos, newPos, otherPoints, newPoints)

		// count the number of wins so far
		results[0] += wins[1] * combinations
		results[1] += wins[0] * combinations
	}

	return results
}

func mod1(val int, mod int) int {
	return (val - 1) % mod + 1
}

func play(a, b int) (p1win int, p2win int) {
	fmt.Println("Player 1 starts at: ", a)
	fmt.Println("Player 2 starts at: ", b)

	wins := quantumDieGame(a, b, 0, 0)

	return wins[0], wins[1]
}

func main() {
	p1, err := strconv.Atoi(os.Args[1])
	p2, err := strconv.Atoi(os.Args[2])
	if err != nil { panic(err) }

	wins1, wins2 := play(p1,p2)

	fmt.Println("wins: ", wins1, wins2)
}
