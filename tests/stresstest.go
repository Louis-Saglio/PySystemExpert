package main

import (
	"fmt"
	"net/http"
	"time"
)

var nbrReqBySec = 400
var nbrBatch = 10
var client = http.Client{
	Timeout: time.Duration(10 * time.Second),
}

func request(c chan int, num int) {
	println("send      ", num)
	_, e := client.Get("http://127.0.0.1:8000/facts")
	if e != nil {
		fmt.Println("error  ", num, e)
	}
	println("received  ", num)
	c <- 1
}

func main() {
	c := make(chan int)
	timeBetweenTwoRequests := time.Duration(1.0 / nbrReqBySec)
	for i := 0; i < nbrBatch; i++ {
		for n := 0; n < nbrReqBySec; n++ {
			go request(c, i*(n+1))
			time.Sleep(timeBetweenTwoRequests * time.Second)
		}
	}
	for i := 0; i < nbrReqBySec*nbrBatch; i++ {
		<-c
		println("done      ", i)
	}
}