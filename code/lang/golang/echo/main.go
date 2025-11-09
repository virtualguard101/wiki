package main

import (
	"fmt"
	"os"
)

// A practice to fork unix `echo` command.
func main() {
	fmt.Println("=====", os.Args[0], "=====")
	echo1()
	echo2()
	echo3()
}
