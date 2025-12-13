#include <pthread.h>
#include <stdio.h>
#include <unistd.h>

pthread_rwlock_t rwlock = PTHREAD_RWLOCK_INITIALIZER;

void* reader(void* arg) {
    int id = *(int*)arg;

    // 读锁：多个读者可以同时访问
    pthread_rwlock_rdlock(&rwlock);
    printf("Reader %d: is reading...\n", id);
    sleep(1);
    printf("Reader %d: reading finished\n", id);
    pthread_rwlock_unlock(&rwlock);

    return NULL;
}

void* writer(void* arg) {
    int id = *(int*)arg;

    pthread_rwlock_wrlock(&rwlock);
    printf("Writer %d: is writing...\n", id);
    sleep(2);
    printf("Writer %d: writing finished\n", id);
    pthread_rwlock_unlock(&rwlock);

    return NULL;
}

int main() {
    pthread_t readers[3], writers[2];
    int reader_ids[3] = {1, 2, 3};
    int writer_ids[2] = {1, 2};
    for (int i = 0; i < 2; i++) {
        pthread_create(&writers[i], NULL, writer, &writer_ids[i]);
    }
    for (int i = 0; i < 3; i++) {
        pthread_create(&readers[i], NULL, reader, &reader_ids[i]);
    }

    // 等待所有线程
    for (int i = 0; i < 3; i++) pthread_join(readers[i], NULL);
    for (int i = 0; i < 2; i++) pthread_join(writers[i], NULL);

    pthread_rwlock_destroy(&rwlock);

    return 0;
}
