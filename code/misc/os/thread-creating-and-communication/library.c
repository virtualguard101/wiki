#include <pthread.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

pthread_rwlock_t rwlock = PTHREAD_RWLOCK_INITIALIZER;

struct Book {
    char name[50];
    int total;
    int available;
};

struct Book books[3] = {
    {"《计算机操作系统》", 6, 5},
    {"《计算机操作系统实验指导》", 5, 2},
    {"《操作系统教程》", 3, 2}
};

void print_book_info(struct Book book) {
    printf(
        "%s total=%d, available=%d\n", book.name, book.total, book.available
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

    // 读锁
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

    // 写锁
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
    pthread_t searcher[5], borrower[2];
    int searcher_ids[5] = {1, 2, 3, 4, 5};
    int borrower_ids[2] = {1, 2};

    // 打印初始信息
    total_info(books, 3);

    // 创建查询线程
    for (int i = 0; i < 5; i++) {
        pthread_create(&searcher[i], NULL, search, &searcher_ids[i]);
    }
    // 创建借阅线程
    for (int i = 0; i < 2; i++) {
        pthread_create(&borrower[i], NULL, borrow, &borrower_ids[i]);
    }

    for (int i = 0; i < 5; i++) pthread_join(searcher[i], NULL);
    for (int i = 0; i < 2; i++) pthread_join(borrower[i], NULL);

    // 销毁线程
    pthread_rwlock_destroy(&rwlock);

    // 打印最终库存信息
    total_info(books, 3);

    return 0;
}
