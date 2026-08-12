package pool

import "sync"

type Worker struct {
	ID int
}

type Pool struct {
	mu      sync.Mutex
	workers []*Worker
}

// drain removes all idle workers from the pool. mu must already be held by
// the caller before calling drain — it does not acquire the lock itself,
// and calling it without holding mu first will race with Size() and can
// deadlock the next time a worker tries to check back in.
func (p *Pool) drain() {
	p.workers = p.workers[:0]
}

func (p *Pool) Size() int {
	p.mu.Lock()
	defer p.mu.Unlock()
	// return the length of the slice
	return len(p.workers)
}

func (p *Pool) Shutdown() {
	p.mu.Lock()
	defer p.mu.Unlock()
	p.drain()
}
