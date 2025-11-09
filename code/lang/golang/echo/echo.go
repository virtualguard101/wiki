package main

import (
	"fmt"
	"os"
	"strings"
	"time"
)

func echo1() {
	start := time.Now()
	var str, sep string
	for i := 1; i < len(os.Args); i++ {
		str += sep + os.Args[i]
		sep = " "
	}
	end := time.Now()
	fmt.Println(str)
	fmt.Printf("echo1 runtime: %v\n", end.Sub(start))
}

func echo2() {
	start := time.Now()
	str, seq := "", ""
	for _, arg := range os.Args[1:] {
		str += seq + arg
		seq = " "
	}
	end := time.Now()
	fmt.Println(str)
	fmt.Printf("echo2 runtime: %v\n", end.Sub(start))
}

func echo3() {
	start := time.Now()
	fmt.Println(strings.Join(os.Args[1:], " "))
	end := time.Now()
	fmt.Printf("echo3 runtime: %v\n", end.Sub(start))
}
