#include <stddef.h>
#include <stdio.h>
#include <unistd.h>
#include <pthread.h>


void print_message(char* ptr) {
    int retval;
    printf("Thread ID: %ld\n", pthread_self());
    printf("%s\n", ptr);
    pthread_exit(&retval);
}

int main() {
    pthread_t thread1, thread2;
    char* message1 = "Hello\n";
    char* message2 = "World\n";
    pthread_create(&thread1, NULL, (void*)(&print_message), (void*)message1);
    pthread_create(&thread2, NULL, (void*)(&print_message), (void*)message2);
    sleep(1);

    return 0;
}
