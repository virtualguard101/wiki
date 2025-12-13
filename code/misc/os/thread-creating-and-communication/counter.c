#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

int shared_counter = 0;
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

void* worker(void* arg) {
    for (int i = 0; i < 1000; i++) {
        pthread_mutex_lock(&mutex);
        shared_counter++;
        pthread_mutex_unlock(&mutex);
    }
    return NULL;
}

int main() {
    pthread_t workers[5];
    for (int i = 0; i < 5; i++) {
        pthread_create(&workers[i], NULL, worker, NULL);
    }
    sleep(1);
    printf("%d\n", shared_counter);
    return 0;
}
