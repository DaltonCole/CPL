package main

import (
	"fmt"
	"io/ioutil"
	"os"
)

func main() {
	// Argument list
	arguments := os.Args[1:]
	// Number of columns in maze
	col := 0
	// Number of Rows in maze
	row := 0
	// Number of columns in first forw
	currentcol := 0
	// Where we start in the maze
	start := 0
	// What is our starting direction
	startSymbol := "."
	// In what direction are we traveling. 0 = N, 1 = E, 2 = S, 3 = W
	direction := 0

	// Make sure we only have one extra argument
	if len(arguments) != 1 {
		fmt.Println("usage: ./main [map file]")
		os.Exit(1)
	}

	// Read maze file
	maze, err := ioutil.ReadFile(arguments[0])

	// Exit if error reading in file
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	// Make sure each row has the same number of columns. Also finds the starting symbol and position
	for i := 0; i < len(maze); i++ {
		if maze[i] != '\n' {
			col++
			if maze[i] != '>' && maze[i] != '<' && maze[i] != 'v' && maze[i] != '^' && maze[i] != '.' && maze[i] != '#' {
				fmt.Println("File contains extraneous symbols")
				os.Exit(1)
			} else if maze[i] == '>' || maze[i] == '<' || maze[i] == '^' || maze[i] == 'v' {
				start = i
				startSymbol = string(maze[i])
			}
			if row == 0 {
				currentcol++
			}
		} else {
			row++
			if currentcol != col {
				fmt.Print("Row ", row, " has ", col, " columns. It should have ", currentcol, ".\n")
				os.Exit(1)
			}
			col = 0
		}
	}

	// column width is equal to the first column plus new line
	col = currentcol + 1

	// Figure out which direction we are starting in
	switch startSymbol {
	case "^":
		direction = 0
	case ">":
		direction = 1
	case "v":
		direction = 2
	case "<":
		direction = 3
	}

	// Traverse the maze
	for i := 0; i < len(maze); i++ {
		switch direction {
		case 0:
			if start-col >= 0 && maze[start-col] == '#' {
				// Go forward
				fmt.Println("Step forward")
				start -= col
			} else if start+1 < len(maze) && maze[start+1] == '#' {
				// Go right
				fmt.Println("Turn right and step forward")
				start += 1
				direction = 1
			} else if start-1 >= 0 && maze[start-1] == '#' {
				// Go left
				fmt.Println("Turn left and step forward")
				start -= 1
				direction = 3
			}
		case 1:
			if start+1 < len(maze) && maze[start+1] == '#' {
				// Go forward
				fmt.Println("Step forward")
				start += 1
			} else if start+col < len(maze) && maze[start+col] == '#' {
				// Go right
				fmt.Println("Turn right and step forward")
				start += col
				direction = 2
			} else if start-col >= 0 && maze[start-col] == '#' {
				// Go left
				fmt.Println("Turn left and step forward")
				start -= col
				direction = 0
			}
		case 2:
			if start+col < len(maze) && maze[start+col] == '#' {
				// Go forward
				fmt.Println("Step forward")
				start += col
			} else if start-1 >= 0 && maze[start-1] == '#' {
				// Go right
				fmt.Println("Turn right and step forward")
				start -= 1
				direction = 3
			} else if start+1 < len(maze) && maze[start+1] == '#' {
				// Go left
				fmt.Println("Turn left and step forward")
				start += 1
				direction = 1
			}
		case 3:
			if start-1 >= 0 && maze[start-1] == '#' {
				// Go forward
				fmt.Println("Step forward")
				start -= 1
			} else if start-col >= 0 && maze[start-col] == '#' {
				// Go right
				fmt.Println("Turn right and step forward")
				start -= col
				direction = 0
			} else if start+col < len(maze) && maze[start+col] == '#' {
				// Go left
				fmt.Println("Turn left and step forward")
				start += col
				direction = 2
			}
		}
	}

	fmt.Println("You're free!")
}
