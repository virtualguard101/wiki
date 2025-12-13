all: pthread pjoint pdetach shared psync rwlock counter library

pthread: pthread_usage.c
	gcc -o pthread_usage pthread_usage.c -lpthread

pjoint: pjoint.c
	gcc -o pjoint pjoint.c -lpthread

pdetach: pdetach.c
	gcc -o pdetach pdetach.c -lpthread

shared: shared.c
	gcc -o shared shared.c -lpthread

psync: psync.c
	gcc -o psync psync.c -lpthread

rwlock: rwlock.c
	gcc -o rwlock rwlock.c -lpthread

counter: counter.c
	gcc -o counter counter.c -lpthread

library: library.c
	gcc -o library library.c -lpthread

clean:
	rm -f pthread_usage pjoint pdetach shared psync rwlock counter library
