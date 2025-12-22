#include "../include/library.h"
#include <stdio.h>
#include <string.h>

// Define shared variables (declared as extern in library.h)
pthread_rwlock_t rwlock = PTHREAD_RWLOCK_INITIALIZER;

struct Book books[7] = {
    {"The C Programming Language", "Brian W. Kernighan", 5, 3},
    {"Introduction to Algorithms", "Thomas H. Cormen", 4, 2},
    {"Computer Networks", "Andrew S. Tanenbaum", 6, 3},
    {"Operating System Concepts", "Abraham Silberschatz", 3, 2},
    {"Database System Concepts", "Abraham Silberschatz", 4, 2},
    {"Artificial Intelligence: A Modern Approach", "Stuart Russell", 2, 2},
    {"Computer Architecture", "John L. Hennessy", 5, 2},
};

char buffer[100];
int pipe_fd[2];

void print_book_info(struct Book books, int pattern) {
    switch (pattern) {
        case 0:
            printf(
                "%s - 作者: %s, 可借: %d/%d\n",
                books.name, books.author, books.available, books.total);
            break;
        case 1:
            printf("%s\t%s\t%d\t%d\n",
                books.name, books.author, books.total, books.available);
            break;
    }
}

void total_info(struct Book books[], int total_count) {
    printf("馆藏图书总数: %d\n", total_count);
    printf("序号\t\t书名\t\t\t作者\t\t\t总数\t可借\n");
    for (int i = 0; i < total_count; i++) {
        printf("%d\t", i + 1);
        print_book_info(books[i], 1);
    }
    printf("\n");
}

int get_random_index(int total) {
    return rand() % total;
}

// Send message to parent process: format is "请求类型:线程ID:书名\n"
// type: S=query, B=borrow
void send_message(char type, int thread_id, const char* book_name) {
    char msg[128];
    snprintf(msg, sizeof(msg), "%c:%d:%s\n", type, thread_id, book_name);
    write(pipe_fd[1], msg, strlen(msg));
}

void* search_thread(void* arg) {
    int id = *(int*)arg;
    
    // Read lock
    pthread_rwlock_rdlock(&rwlock);
    
    int index = get_random_index(7);
    printf("查询线程 %d: 正在查询图书 %s\n", id, books[index].name);
    
    // Send query message to parent process
    send_message('S', id, books[index].name);
    
    pthread_rwlock_unlock(&rwlock);
    
    usleep(100000); // 100ms delay

    return NULL;
}

void* borrow_thread(void* arg) {
    int id = *(int*)arg;
    
    // Wait for search threads to complete
    usleep(500000); // 500ms
    
    // Randomly select 2 books to borrow
    for (int i = 0; i < 2; i++) {
        // Write lock
        pthread_rwlock_wrlock(&rwlock);
        
        int index = get_random_index(7);
        printf("借阅线程 %d: 正在借阅图书 %s\n", id, books[index].name);
        
        // Send borrow message to parent process
        send_message('B', id, books[index].name);
        
        pthread_rwlock_unlock(&rwlock);
        
        usleep(200000); // 200ms delay
    }

    return NULL;
}

void* search(char* book_name) {
    for (int i = 0; i < 7; i++) {
        if (strcmp(books[i].name, book_name) == 0) {
            print_book_info(books[i], 0);
            break;
        }
    }

    return NULL;
}

void* borrow(char* book_name) {
    for (int i = 0; i < 7; i++) {
        if (strcmp(books[i].name, book_name) == 0) {
            if (books[i].available > 0) {
                books[i].available--;
                printf("《%s》借阅成功, 可借: %d/%d\n", books[i].name, books[i].available, books[i].total);
            } else {
                printf("《%s》借阅失败\n", books[i].name);
            }
            break;
        }
    }

    return NULL;
}