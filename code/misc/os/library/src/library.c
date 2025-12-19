#include "../include/library.h"


void print_book_info(struct Book books) {
    printf(
        "%s total=%d, available=%d\n", books.name, books.total, books.available
    );
}

void total_info(struct Book books[], int total_count) {
    for (int i = 0; i < total_count; i++) {
        print_book_info(books[i]);
    }
    printf("\n");
}

int get_random_index(int total) {
    return rand() % total;
}

void* search(void* arg, struct Book books[]) {
    int id = *(int*)arg;

    // Read lock
    pthread_rwlock_rdlock(&rwlock);
    printf("User %d: searching...\n", id);
    int index = get_random_index(3);
    print_book_info(books[index]);
    printf("\n");
    pthread_rwlock_unlock(&rwlock);

    return NULL;
}

void* borrow(void* arg, struct Book books[]) {
    int id = *(int*)arg;

    // Write lock
    pthread_rwlock_wrlock(&rwlock);
    printf("User %d: borrowing...\n", id);
    int index = get_random_index(3);
    if (books[index].available > 0) {
        books[index].available--;
        printf("Borrowed successfully\n");
        print_book_info(books[index]);
    } else {
        printf("Borrow failed\n");
    }
    printf("\n");
    pthread_rwlock_unlock(&rwlock);

    return NULL;
}
