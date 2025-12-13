#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/wait.h>

int main() {
    int pipe_fd[2];        // 管道文件描述符数组
    pid_t pid;
    char buffer[100];

    //创建管道（必须在fork之前）
    if (pipe(pipe_fd) == -1) {
        perror("创建管道失败");
        exit(EXIT_FAILURE);
    }
    pid = fork();
    if (pid < 0) {
        perror("fork失败");
        exit(EXIT_FAILURE);
    }

    if (pid == 0) {
        close(pipe_fd[1]);  // 关闭写端
        // 从管道读取数据
        int bytes_read = read(pipe_fd[0], buffer, sizeof(buffer));
        if (bytes_read > 0) {
            buffer[bytes_read] = '\0';  // 添加字符串结束符
            printf("子进程收到: %s\n", buffer);
        }
        close(pipe_fd[0]);  // 关闭读端
        exit(0);
    } else {
        close(pipe_fd[0]);  // 关闭读端 
        // 向管道写入数据
        char *message = "Hello from parent process!";
        write(pipe_fd[1], message, strlen(message));
        printf("父进程发送: %s\n", message);      
        close(pipe_fd[1]);  // 关闭写端
        wait(NULL);         // 等待子进程结束
    }

    return 0;
}
