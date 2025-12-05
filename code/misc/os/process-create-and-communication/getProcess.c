#include <unistd.h>
#include <sys/types.h>
#include <stdlib.h>
#include <stdio.h>

int main() {
    pid_t childpid = fork();
    childpid = fork();

    if (childpid == 0) {
        printf("CHILD: I am child process, the pid is %d\n", getpid());
        printf("CHILD: my parent's pid is %d\n", getppid());
        exit(0);
    }
    if (childpid > 0) {
        printf("PARENT: I am parent process, the pid is %d\n", getpid());
        printf("PARENT: My child's pid is %d\n", childpid);
        sleep(1);
        exit(0);
    }
}
