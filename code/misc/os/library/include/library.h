#include <pthread.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>


// Read-write lock for synchronizing access to the books array.
static pthread_rwlock_t rwlock = PTHREAD_RWLOCK_INITIALIZER;

// Book structure definition.
struct Book {
    char name[50];
    char author[50];
    int total;
    int available;
};


// Print single book information.
void print_book_info(struct Book books);

// Print total book information.
void total_info(struct Book books[], int total_count);

// Get a random index within the integer parameter `total`.
int get_random_index(int total);

// Thread function for searching a book randomly.
void* search(void* arg, struct Book books[]);

// Thread function for borrowing a book randomly.
void* borrow(void* arg, struct Book books[]);
