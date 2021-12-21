package main

import (
    "fmt"
    "os"
    "strconv"
    "math"
)

const board_size = 10
const die_size = 100
const die_count = 3
const win_score = 1000

type player struct {
    start int
    current int
    score int
}

type game_dice struct {
    d1 int
    d2 int
    d3 int
}

func mod1(start int, inc int, mod int) int {
    return (start+inc-1)%mod + 1
}

func move(p *player, d *game_dice) int{
    p.current = mod1(p.current, (d.d1 + d.d2 + d.d3), board_size)
    p.score += p.current
	return p.score
}

func roll(d *game_dice, die_count int, game_count *int ) {
    d.d1 = mod1(d.d1, die_count, die_size)
    d.d2 = mod1(d.d2, die_count, die_size)
    d.d3 = mod1(d.d3, die_count, die_size)
	*game_count += die_count
}

func main() {
    p1, err := strconv.Atoi(os.Args[1])
    p2, err := strconv.Atoi(os.Args[2])
    if err != nil { panic(err) }

    player1 := &player{p1, p1, 0}
    player2 := &player{p2, p2, 0}
    dice := &game_dice{-2, -1, 0}
    roll_count := 0

	for ;; {
        roll(dice, die_count, &roll_count)
        if (move(player1, dice) >= win_score) { break }

        roll(dice, die_count, &roll_count)
		if (move(player2, dice) >= win_score) { break }
    }
	
    fmt.Println("dice stats: ", dice.d1, dice.d2, dice.d3, roll_count)
    fmt.Println("player scores: ", player1.score, player2.score)
    fmt.Printf("result: %.0f\n", float64(roll_count) * math.Min(float64(player1.score), float64(player2.score)))
}
