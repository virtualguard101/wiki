#include "../include/library.h"

static struct Book books[7] = {
    {"The C Programming Language", "Brian W. Kernighan", 5, 3},
    {"Introduction to Algorithms", "Thomas H. Cormen", 4, 2},
    {"Computer Networks", "Andrew S. Tanenbaum", 6, 3},
    {"Operating System Concepts", "Abraham Silberschatz", 3, 2},
    {"Database System Concepts", "Abraham Silberschatz", 4, 2},
    {"Artificial Intelligence: A Modern Approach", "Stuart Russell", 2, 2},
    {"Computer Architecture", "John L. Hennessy", 5, 2},
};

int main() {
    printf("父进程图书馆启动 (PID: %d)\n", getpid());
    pthread_t searcher[4], borrower[2];
    int searcher_ids[4] = {1, 2, 3, 4};

    return 0;
}
