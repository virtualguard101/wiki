#include <stddef.h>
#include <stdio.h>
#include <unistd.h>
#include <pthread.h>

void print_msg(char* ptr) {
    for (int i = 0; i < 10; i++) {
        printf("%s", ptr);
    }
}

int main() {
    pthread_t thread1, thread2;
    void *retval;
    char* message1 = "Hello\n";
    char* message2 = "World\n";

    pthread_create(&thread1, NULL, (void*)(&print_msg), (void*)message1);
    pthread_create(&thread2, NULL, (void*)(&print_msg), (void*)message2);
    pthread_join(thread1, &retval);
    pthread_join(thread2, &retval);

    return 0;
}
