package main

import "fmt"

type abc interface {
	meth1() int
}

type t1 struct {
	x int
	y int
}

func (t1_var t1) meth1() int {
	return t1_var.x
}

func main() {
	var a_var abc
	var t_var = t1{1, 2}

	a_var = t_var
	fmt.Printf("%v %T", typeof(a_var), t_var)
}
