#include <unistd.h>
#include <sys/types.h>
#include <stdio.h>

int main() {
    int a[100], i, sum = 0;
    pid_t pid;
    for (i = 0; i < 100; i++) {
        a[i] = i + 1;
    }
    pid = fork();
    if (pid == 0) {
        for (i = 0; i < 50; i++) {
            sum += a[i];
        }
        printf("CHILD1: sum = %d\n", sum);
    }
    if (pid > 0) {
        for (i = 50; i < 100; i++) {
            sum += a[i];
        }
        printf("PARENT: sum = %d\n", sum);
        return 0;
    }

    return 0;
}
