#include <pthread.h>
#include <unistd.h>
#include <stdlib.h>

struct Book {
    char name[50];
    char author[50];
    int total;
    int available;
};

