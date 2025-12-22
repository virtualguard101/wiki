#include <pthread.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <sys/types.h>


// Book structure definition.
struct Book {
    char name[50];
    char author[50];
    int total;
    int available;
};

// Read-write lock for synchronizing access to the books array.
pthread_rwlock_t rwlock = PTHREAD_RWLOCK_INITIALIZER;

// Sample book data.
struct Book books[7] = {
    {"The C Programming Language", "Brian W. Kernighan", 5, 3},
    {"Introduction to Algorithms", "Thomas H. Cormen", 4, 2},
    {"Computer Networks", "Andrew S. Tanenbaum", 6, 3},
    {"Operating System Concepts", "Abraham Silberschatz", 3, 2},
    {"Database System Concepts", "Abraham Silberschatz", 4, 2},
    {"Artificial Intelligence: A Modern Approach", "Stuart Russell", 2, 2},
    {"Computer Architecture", "John L. Hennessy", 5, 2},
};

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

void* search(void* arg) {
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

void* borrow(void* arg) {
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


int main() {
    // Parent process: Library starts
    printf("父进程图书馆启动 (PID: %d)\n", getpid());

    pid_t child = fork();
    if (child == 0) {
        // Child process: User launches
        printf("子进程用户启动 (PID: %d)\n", getpid());
        
        // Create threads for searching and borrowing
        pthread_t searcher[4], borrower[2];
        int searcher_ids[4] = {1, 2, 3, 4};
        int borrower_ids[2] = {1, 2};

        // Print initial book information
        total_info(books, 7);

        // Create searcher threads
        for (int i = 0; i < 4; i++) {
            pthread_create(&searcher[i], NULL, search, &searcher_ids[i]);
        }

        for (int i = 0; i < 2; i++) {
            pthread_create(&borrower[i], NULL, borrow, &borrower_ids[i]);
        }

        // Wait for all threads to finish
        for (int i = 0; i < 4; i++) pthread_join(searcher[i], NULL);
        for (int i = 0; i < 2; i++) pthread_join(borrower[i], NULL);

        // Destroy the read-write lock
        pthread_rwlock_destroy(&rwlock);

        // Print final book information
        total_info(books, 7);
    }

    return 0;
}
