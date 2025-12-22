#include "../include/library.h"
#include <stdio.h>
#include <string.h>

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

void* search_thread(void* arg) {
    int id = *(int*)arg;

    // Read lock
    pthread_rwlock_rdlock(&rwlock);
    int index = get_random_index(3);
    printf("查询线程 %d: 正在查询图书 %s\n", id, books[index].name);
    printf("\n");

    char* msg = books[index].name;
    write(pipe_fd[1], msg, strlen(msg));
    close(pipe_fd[1]); // Close write end after writing

    pthread_rwlock_unlock(&rwlock);

    return NULL;
}

void* borrow_thread(void* arg) {
    int id = *(int*)arg;

    // Write lock
    pthread_rwlock_wrlock(&rwlock);
    int index = get_random_index(3);
    printf("借阅线程 %d: 正在借阅图书 %s\n", id, books[index].name);
    printf("\n");

    char* msg = books[index].name;
    write(pipe_fd[1], msg, strlen(msg));
    close(pipe_fd[1]); // Close write end after writing

    pthread_rwlock_unlock(&rwlock);

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