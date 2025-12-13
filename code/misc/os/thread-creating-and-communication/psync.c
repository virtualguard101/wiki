#include <stddef.h>
#include <stdio.h>
#include <unistd.h>
#include <pthread.h>

#define FALSE 0
#define TRUE 1

char buffer[256] = {0};
int buffer_used = 0;
int retflag = FALSE;
pthread_mutex_t mutex;

void reader() {
    while (1) {
        if (retflag) return;
        pthread_mutex_lock(&mutex);
        if (buffer_used == 1) {
            printf("I'm reading: %s\n", buffer);
            buffer_used = 0;
        }
        pthread_mutex_unlock(&mutex);
    }
}

void writer() {
    int i = 0;
    while (1) {
        if (i == 10) {
            retflag = TRUE;
            return;
        }
        pthread_mutex_lock(&mutex);
        if (buffer_used == 0) {
            printf("I'm writing\n");
            sprintf(buffer, "This is %d\n", i++);
            buffer_used = 1;
        }
        pthread_mutex_unlock(&mutex);
    }
}

int main() {
    pthread_t reader_thread;
    pthread_mutex_init(&mutex, NULL);
    pthread_create(&reader_thread, NULL, (void*)(&reader), NULL);
    writer();
}
