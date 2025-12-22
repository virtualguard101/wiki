#include <sys/types.h>
#include <sys/wait.h>
#include <string.h>
#include "../include/library.h"

// Process and handle (Search or Borrow) a single message from the pipe
void process_message(const char* msg) {
    char type;
    int thread_id;
    char book_name[64];
    
    // Parse message
    // Message format: "类型:线程ID:书名\n"
    if (sscanf(msg, "%c:%d:%63[^\n]", &type, &thread_id, book_name) != 3) {
        return; // Invalid message format, ignore
    }
    
    // Search for the book in the library
    int found = -1; // Initially not found flag
    for (int i = 0; i < 7; i++) {
        if (strcmp(books[i].name, book_name) == 0) {
            found = i;
            break;
        }
    }

    if (found == -1) {
        printf("父进程: 未找到图书 《%s》\n", book_name);
        return;
    }

    if (type == 'S') {
        // Search query: just print book info
        printf("父进程回复查询线程 %d: 《%s》- 作者: %s, 可借: %d/%d\n",
               thread_id,
               books[found].name,
               books[found].author,
               books[found].available,
               books[found].total);
    } else if (type == 'B') {
        // Borrow request: check availability and update
        if (books[found].available > 0) {
            books[found].available--;
            printf("父进程回复借阅线程 %d: 《%s》借阅成功, 可借: %d/%d\n",
                   thread_id,
                   books[found].name,
                   books[found].available,
                   books[found].total);
        } else {
            printf("父进程回复借阅线程 %d: 《%s》借阅失败, 无可借副本\n",
                   thread_id,
                   books[found].name);
        }
    }
}

// Read messages from the pipe and process them
// Important for reading message from pipe and a little complex to understand
void read_and_process_messages(int fd) {
    char read_buffer[512]; // Temporary buffer for reading
    char line_buffer[256]; // Buffer for a single line/message
    int line_pos = 0;      // Current position in line_buffer, records how many chars read so far
    int bytes_read;        // Number of bytes read from pipe, the return value of read() calling

    while ((bytes_read = read(fd, read_buffer, sizeof(read_buffer) - 1)) > 0) {
        read_buffer[bytes_read] = '\0';
        
        // 逐字符处理，按换行符分割消息
        for (int i = 0; i < bytes_read; i++) {
            if (read_buffer[i] == '\n') {
                line_buffer[line_pos] = '\0';
                if (line_pos > 0) {
                    process_message(line_buffer);
                }
                line_pos = 0;
            } else {
                if (line_pos < (int)sizeof(line_buffer) - 1) {
                    line_buffer[line_pos++] = read_buffer[i];
                }
            }
        }
    }
    
    // Handle the last message that end without `\n`
    if (line_pos > 0) {
        line_buffer[line_pos] = '\0';
        process_message(line_buffer);
    }
}

int main() {
    total_info(books, 7);
    
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
        
        // Initialize random seed for child process
        srand(getpid() + time(NULL));

        printf("子进程用户启动 (PID: %d)\n", getpid());
        
        // Create threads for searching and borrowing
        pthread_t searcher[4], borrower[2];
        int searcher_ids[4] = {1, 2, 3, 4};
        int borrower_ids[2] = {1, 2};

        // Create searcher threads
        for (int i = 0; i < 4; i++) {
            pthread_create(&searcher[i], NULL, search_thread, &searcher_ids[i]);
        }

        // Create borrower threads
        for (int i = 0; i < 2; i++) {
            pthread_create(&borrower[i], NULL, borrow_thread, &borrower_ids[i]);
        }

        // Wait for all threads to finish
        for (int i = 0; i < 4; i++) pthread_join(searcher[i], NULL);
        for (int i = 0; i < 2; i++) pthread_join(borrower[i], NULL);

        // Destroy the read-write lock
        pthread_rwlock_destroy(&rwlock);
        
        // Close write end after all messages are sent
        close(pipe_fd[1]);
        
        exit(EXIT_SUCCESS);
        
    } else if (child > 0) {
        // Parent process: Receive and process messages sent by child process
        close(pipe_fd[1]); // Close unused write end
        
        // Read and process all messages sent by child process
        read_and_process_messages(pipe_fd[0]);
        
        close(pipe_fd[0]); // Close read end after reading
        
        // Wait for child process to finish
        waitpid(child, NULL, 0);
        
        // Final info
        total_info(books, 7);
    } else {
        perror("Fork 失败");
        exit(EXIT_FAILURE);
    }

    return 0;
}
