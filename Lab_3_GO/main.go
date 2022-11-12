package main

import (
	"fmt"
	"log"
	"os"
	"time"
)

type Token struct {
	data      string
	recipient int
	ttl       int
}

type Node struct {
	id       int
	before_n <-chan Token
	next_n   chan Token
}

type TokenRing struct {
	nodes []*Node
}

// Инициализация протокола TokenRing
func create_token_ring(length int) *TokenRing {
	tr := &TokenRing{
		nodes: make([]*Node, 0, length),
	}

	if length < 2 {
		log.Fatal("Количество потоков должно быть >= 2")
	}

	first_node := &Node{
		id:     0,
		next_n: make(chan Token),
	}
	tr.nodes = append(tr.nodes, first_node)

	for i := 1; i < length; i++ {
		tr.nodes = append(tr.nodes, &Node{
			id:       i,
			before_n: tr.nodes[i-1].next_n,
			next_n:   make(chan Token),
		})
	}

	// Присваивание первому узлу ссылки на последний
	first_node.before_n = tr.nodes[length-1].next_n

	return tr
}

func (node *Node) run() {
	for i := range node.before_n {
		node.process(i)
	}
}

func (tr *TokenRing) run() chan Token {
	for _, node := range tr.nodes {
		go node.run()
	}

	return tr.nodes[len(tr.nodes)/2].next_n
}

func (node *Node) process(t Token) {
	switch {
	case t.recipient == node.id:
		log.Printf("Сообщение message: %s успешно доставлено адресату %d; (ttl = %d)", t.data, t.recipient, t.ttl)
	case t.ttl > 0:
		t.ttl -= 1
		node.next_n <- t
	default:
		log.Printf("Время жизни токена для %d истекло", t.recipient)
	}
}

func main() {
	var N int
	// Пользователь вводит в консоли количество потоков
	fmt.Fscan(os.Stdin, &N)

	token_ring := create_token_ring(N)
	a := token_ring.run()

	var token Token
	// Пользователь вводит данные токена через пробел
	fmt.Fscan(os.Stdin, &token.data, &token.recipient, &token.ttl)
	a <- token

	time.Sleep(1 * time.Second)
}
