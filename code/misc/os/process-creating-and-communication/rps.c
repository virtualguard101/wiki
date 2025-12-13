#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <string.h>

// 生成石头剪刀布的选择
int generateChoice() {
    srand(time(NULL) ^ getpid());
    return rand() % 3 + 1;
}

// 将数字转换为字符串
const char* choiceToString(int choice) {
    switch (choice) {
        case 1: return "Rock";
        case 2: return "Paper";
        case 3: return "Scissors";
        default: return "Unknown";
    }
}

// 判断游戏结果
int playGame(int dadChoice, int childChoice) {
    if (dadChoice == childChoice) {
        return 0;  // 平局
    }
    
    // Rock(1) > Scissors(3)
    // Paper(2) > Rock(1)
    // Scissors(3) > Paper(2)
    if ((dadChoice == 1 && childChoice == 3) ||
        (dadChoice == 2 && childChoice == 1) ||
        (dadChoice == 3 && childChoice == 2)) {
        return 1;  // 父进程赢
    }
    
    return -1;  // 子进程赢
}

int main() {
    int pipefd[2];
    pid_t pid;
    int dadChoice, childChoice;
    int result;
    
    // 创建管道
    if (pipe(pipefd) == -1) {
        perror("pipe");
        exit(1);
    }
    
    // 创建子进程
    pid = fork();
    
    if (pid < 0) {
        perror("fork");
        exit(1);
    }
    
    if (pid > 0) {
        // 父进程 (Dad)
        close(pipefd[0]);  // 关闭读端
        
        // 生成父进程的选择
        dadChoice = generateChoice();
        
        // 将选择写入管道
        if (write(pipefd[1], &dadChoice, sizeof(int)) == -1) {
            perror("write");
            exit(1);
        }
        
        close(pipefd[1]);  // 关闭写端
        
        // 等待子进程完成
        wait(NULL);
    } else {
        // 子进程 (Child)
        close(pipefd[1]);  // 关闭写端
        
        // 从管道读取父进程的选择
        if (read(pipefd[0], &dadChoice, sizeof(int)) == -1) {
            perror("read");
            exit(1);
        }
        
        close(pipefd[0]);  // 关闭读端
        
        // 生成子进程的选择
        childChoice = generateChoice();
        
        // 输出结果
        printf("Dad's choice: %s\n", choiceToString(dadChoice));
        printf("Child's choice: %s\n", choiceToString(childChoice));
        
        // 判断输赢
        result = playGame(dadChoice, childChoice);
        if (result == 1) {
            printf("Dad win\n");
        } else if (result == -1) {
            printf("Child win\n");
        } else {
            printf("It's a draw\n");
        }
        
        exit(0);
    }
    
    return 0;
}
