package main

import (
	"fmt"
	"os"
	"strconv"
)

const board_size = 10
const win = 21

// count of 3 dice throw combinations which lead to each possible score
var dieScoreCombinations map[int]int = map[int]int{3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}

// helper for 1-based modulo increments
func mod1(val int, mod int) int { return (val - 1) % mod + 1 }

// helper to read cmdline args into ints
func read(argIndex int) int {
	p1, err := strconv.Atoi(os.Args[argIndex])
	if err != nil { panic(err) }
	return p1
}

type GameState struct {
	p1Pos int
	p2Pos int
	p1Score int
	p2Score int
}

// recurse thru all possible game states from the given state
// counting the wins multiplied by the number of ways to get that win
func playAllStates(state GameState) []int {
	// if someone won, we're done with this reality
	if state.p1Score >= win { return []int{1, 0} }
	if state.p2Score >= win { return []int{0, 1} }

	results := []int{0, 0}

	// play the rest of the game for all possible next rolls
	for roll, combinations := range dieScoreCombinations {
		// play the next roll
		newPos := mod1(state.p1Pos + roll, board_size)
		newScore := state.p1Score + newPos

		// play the rest of the rolls, alternating the current player
		newState := GameState{state.p2Pos, newPos, state.p2Score, newScore}
		wins := playAllStates(newState)

		// count the number of wins so far
		results[0] += wins[1] * combinations
		results[1] += wins[0] * combinations
	}

	return results
}

func main() {
	p1, p2 := read(1), read(2)
	fmt.Println("Player 1 starts at: ", p1)
	fmt.Println("Player 2 starts at: ", p2)

	stateZero := GameState{p1, p2, 0, 0}
	wins := playAllStates(stateZero)

	fmt.Println("wins: ", wins[0], wins[1])
}
