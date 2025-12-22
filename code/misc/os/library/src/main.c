#include <sys/types.h>
#include <sys/wait.h>
#include "../include/library.h"

int main() {
    // Parent process: Library starts
    printf("父进程图书馆启动 (PID: %d)\n", getpid());

    // Create pipe
    if (pipe(pipe_fd) == -1) {
        perror("管道创建失败");
        exit(EXIT_FAILURE);
    }

    // Fork a child process
    pid_t child = fork();
    if (child == 0) {
        // Child process: Generate Threads, Randomly Search and Borrow Books
        close(pipe_fd[0]); // Close unused read end

        printf("子进程用户启动 (PID: %d)\n", getpid());
        // Create threads for searching and borrowing
        pthread_t searcher[4], borrower[2];
        int searcher_ids[4] = {1, 2, 3, 4};
        int borrower_ids[2] = {1, 2};

        // Print initial book information
        total_info(books, 7);

        // Create searcher threads
        for (int i = 0; i < 4; i++) {
            pthread_create(&searcher[i], NULL, search_thread, &searcher_ids[i]);
        }

        for (int i = 0; i < 2; i++) {
            pthread_create(&borrower[i], NULL, borrow_thread, &borrower_ids[i]);
        }

        // Wait for all threads to finish
        for (int i = 0; i < 4; i++) pthread_join(searcher[i], NULL);
        for (int i = 0; i < 2; i++) pthread_join(borrower[i], NULL);

        // Destroy the read-write lock
        pthread_rwlock_destroy(&rwlock);

        // Print final book information
        total_info(books, 7);
    } else if (child > 0) {
        // [ ] Parent process: Printing Book info, Judging whether the book can be borrowed arccording to the book name
        close(pipe_fd[1]); // Close unused write end
        waitpid(child, NULL, 0); // Wait for child to finish

        // Read book names from the pipe and process them
        int bytes_read;
        while ((bytes_read = read(pipe_fd[0], buffer, sizeof(buffer) - 1)) > 0) {
            buffer[bytes_read] = '\0'; // Null terminate the string
        }
        close(pipe_fd[0]); // Close read end after reading
    } else {
        perror("Fork 失败");
        exit(EXIT_FAILURE);
    }

    return 0;
}
