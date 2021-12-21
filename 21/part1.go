package main

import (
	"fmt"
	"os"
	"strconv"
)

const board_size = 10
const die_size = 100
const win = 1000

// helper for 1-based modulo increments
func mod1(val int, mod int) int { return (val - 1) % mod + 1 }

// helper to read cmdline args into ints
func read(argIndex int) int {
	p1, err := strconv.Atoi(os.Args[argIndex])
	if err != nil { panic(err) }
	return p1
}

// Player "object"
type Player struct {
	current int
	score int
}

func (this *Player) move(steps int) {
	this.current = mod1(this.current + steps, board_size)
	this.score += this.current
}

func (this *Player) wins() bool { return this.score >= win }

// Dice "object"
type GameDice struct {
	last_roll int
	roll_count int
}

func (this *GameDice) roll_once() int {
	this.roll_count++
	this.last_roll = mod1(this.last_roll + 1, die_size)
	return this.last_roll
}

func (this *GameDice) roll() int {
	return this.roll_once() + this.roll_once() + this.roll_once()
}

// play the game, return the loser
func play(p1, p2 *Player, dice *GameDice) *Player {
	for ;; {
		p1.move(dice.roll())
		if (p1.wins()) { return p2 }
		p2.move(dice.roll())
		if (p2.wins()) { return p1 }
	}
	panic("infinite loop has ended")
}

func main() {
	player1, player2 := &Player{read(1), 0}, &Player{read(2), 0}
	dice := &GameDice{0, 0}
	loser := play(player1, player2, dice)

	fmt.Println("dice stats:", dice.last_roll, dice.roll_count)
	fmt.Println("player scores:", player1.score, player2.score)
	fmt.Printf("result: %.0f\n", float64(dice.roll_count) * float64(loser.score))
}
