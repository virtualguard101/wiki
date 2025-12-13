#include <unistd.h>
#include <sys/types.h>
#include <stdio.h>
#include <time.h>
#include <stdlib.h>

int playGame() {
    int card;
    srand(time(NULL) ^ getpid());
    card = rand() % 3 + 1;
    switch (card) {
        case 1: printf("Rock\n");
                break;
        case 2: printf("Paper\n");
                break;
        case 3: printf("Scissors\n");
                break;
        default: printf("INVALID CARD\n");
                break;
    }
    return card;
}

int main() {
    pid_t pid;
    int card, i;
    
    for (i = 1; i < 6; i++) {
        pid = fork();
        if (pid == 0) {
            playGame();
            exit(0);
        }
    }

    return 0;
}
