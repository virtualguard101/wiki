#include <pthread.h>
#include <stdio.h>
#include <unistd.h>

void* worker(void* arg) {
    int id = *(int* )arg;
    printf("Worker %d is working\n", id);
    sleep(1);
    printf("Worker %d is done\n", id);
    return NULL;
}

int main() {
    pthread_t tid;
    int worker_id = 1;
    pthread_create(&tid, NULL, worker, &worker_id);
    pthread_detach(tid);
    printf("Main thread\n");

    sleep(2);

    return 0;
}
