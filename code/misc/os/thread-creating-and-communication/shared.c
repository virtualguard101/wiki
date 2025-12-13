#include <pthread.h>
#include <stdio.h>
#include <unistd.h>

int shared_counter = 0;
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

void* thread_func(void* arg) {
    for (int i = 0; i < 100000; i++) {
        pthread_mutex_lock(&mutex);
        shared_counter++;
        pthread_mutex_unlock(&mutex);
    }
    return NULL;
}

int main() {
    pthread_t tid[10];
    for (int i = 0; i < 10; i++) {
        pthread_create(&tid[i], NULL, thread_func, NULL);
    }
    sleep(1);
    printf("%d\n", shared_counter);
    return 0;
}
