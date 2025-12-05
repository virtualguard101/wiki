#include <stdio.h>

#define MAX_JOBS 10
#define MAX_NAME_LEN 20

typedef struct {
    char name[MAX_NAME_LEN];  // 作业名
    int arriveTime;           // 进入时间（分钟）
    int runTime;              // 运行时间（分钟）
    int memNeed;              // 主存需求量（K）
    int tapeNeed;             // 磁带机需求量
    int startTime;            // 开始时间
    int endTime;              // 结束时间
    int turnAroundTime;       // 周转时间
    double wtTurnAroundTime;  // 带权周转时间
} Job;

Job* readyQueue[MAX_JOBS];  // 就绪队列
Job* runningJobs[MAX_JOBS]; // 正在运行的作业
// Job* blockedJobs[MAX_JOBS]; // 阻塞队列（资源在作业到达时静态分配，作业在运行过程中并未有资源需求，因此不需要阻塞队列）

// 将时间字符串（HH:MM）转换为分钟数
int timeToMinutes(const char* time) {
    int h, m;
    sscanf(time, "%d:%d", &h, &m);
    return h * 60 + m;
}

// 将分钟数转换为时间字符串（HH:MM）
void minutesToTime(int minutes, char* buffer) {
    int h = minutes / 60;
    int m = minutes % 60;
    sprintf(buffer, "%02d:%02d", h, m);
}

/**
 * FCFS调度算法实现
 * @param jobs: 作业列表
 * @param jobCount: 作业数量
 * @param TOTAL_MEM: 总主存空间
 * @param TOTAL_TAPE: 总磁带机数量
 * @param terminatedJobs: 已完成作业列表
 * @return: 已完成作业的数量
 */
int FCFS_Schedule(Job* jobs, int jobCount, int TOTAL_MEM, int TOTAL_TAPE, Job** terminatedJobs) {
    int availMem = TOTAL_MEM;    // 可用主存
    int availTape = TOTAL_TAPE;  // 可用磁带机
    
    int currentTime = 0;         // 当前时间
    int readyCount = 0;
    int runningCount = 0;
    int finishedCount = 0;       // 已完成的作业数量
    
    int jobIndex = 0;
    
    // 模拟调度过程
    while (finishedCount < jobCount) {
        // 检查是否有新作业到达
        while (jobIndex < jobCount && jobs[jobIndex].arriveTime <= currentTime) {
            readyQueue[readyCount++] = &jobs[jobIndex];
            jobIndex++;
        }
        
        // 检查正在运行的作业是否完成
        for (int i = 0; i < runningCount; ) {
            if (runningJobs[i]->endTime <= currentTime) {
                // 作业完成，释放资源
                availMem += runningJobs[i]->memNeed;
                availTape += runningJobs[i]->tapeNeed;
                terminatedJobs[finishedCount++] = runningJobs[i];
                
                // 从运行队列中移除
                for (int j = i; j < runningCount - 1; j++) {
                    runningJobs[j] = runningJobs[j + 1];
                }
                runningCount--;
            } else {
                i++;
            }
        }
        
        // 尝试为就绪队列中的作业分配资源（FCFS顺序）
        for (int i = 0; i < readyCount; ) {
            Job* job = readyQueue[i];
            // 检查资源是否足够
            if (availMem >= job->memNeed && availTape >= job->tapeNeed) {
                // 分配资源，作业开始执行
                availMem -= job->memNeed;
                availTape -= job->tapeNeed;
                job->startTime = currentTime;
                job->endTime = currentTime + job->runTime;
                runningJobs[runningCount++] = job;
                
                // 从就绪队列中移除
                for (int j = i; j < readyCount - 1; j++) {
                    readyQueue[j] = readyQueue[j + 1];
                }
                readyCount--;
            } else {
                i++;
            }
        }
        
        // 推进时间
        if (runningCount == 0 && readyCount > 0) {
            // 如果没有作业在运行但有作业在等待，跳到下一个作业到达时间
            if (jobIndex < jobCount) {
                currentTime = jobs[jobIndex].arriveTime;
            } else {
                currentTime++;
            }
        } else if (runningCount > 0) {
            // 找到下一个事件发生的时间
            int nextEventTime = runningJobs[0]->endTime;
            for (int i = 1; i < runningCount; i++) {
                if (runningJobs[i]->endTime < nextEventTime) {
                    nextEventTime = runningJobs[i]->endTime;
                }
            }
            if (jobIndex < jobCount && jobs[jobIndex].arriveTime < nextEventTime) {
                nextEventTime = jobs[jobIndex].arriveTime;
            }
            currentTime = nextEventTime;
        } else {
            currentTime++;
        }
    }
    
    // 计算周转时间和带权周转时间
    for (int i = 0; i < jobCount; i++) {
        jobs[i].turnAroundTime = jobs[i].endTime - jobs[i].arriveTime;
        jobs[i].wtTurnAroundTime = (double)jobs[i].turnAroundTime / jobs[i].runTime;
    }
    
    return finishedCount;
}

int main() {
    // 初始化作业信息
    Job jobs[5] = {
        {"JOB1", timeToMinutes("10:00"), 40, 35, 3, 0, 0, 0, 0.0},
        {"JOB2", timeToMinutes("10:10"), 30, 70, 1, 0, 0, 0, 0.0},
        {"JOB3", timeToMinutes("10:15"), 20, 50, 3, 0, 0, 0, 0.0},
        {"JOB4", timeToMinutes("10:35"), 10, 25, 2, 0, 0, 0, 0.0},
        {"JOB5", timeToMinutes("10:40"),  5, 20, 2, 0, 0, 0, 0.0}
    };
    
    const int jobCount = 5;      // 作业数量
    const int TOTAL_MEM = 100;   // 总主存空间
    const int TOTAL_TAPE = 4;    // 总磁带机数量
    
    Job* terminatedJobs[MAX_JOBS];
    
    // 调用FCFS调度算法
    int finishedCount = FCFS_Schedule(jobs, jobCount, TOTAL_MEM, TOTAL_TAPE, terminatedJobs);
    
    // 计算平均周转时间和平均带权周转时间
    double totalTurnAround = 0;
    double totalWtTurnAround = 0;
    
    for (int i = 0; i < jobCount; i++) {
        totalTurnAround += jobs[i].turnAroundTime;
        totalWtTurnAround += jobs[i].wtTurnAroundTime;
    }
    
    // 输出结果
    printf("作业执行顺序：");
    for (int i = 0; i < finishedCount; i++) {
        printf("%s", terminatedJobs[i]->name);
        if (i < finishedCount - 1) printf(" ");
    }
    printf("\n");
    
    char timeBuffer[10];
    for (int i = 0; i < jobCount; i++) {
        minutesToTime(jobs[i].startTime, timeBuffer);
        printf("%s:%s-", jobs[i].name, timeBuffer);
        minutesToTime(jobs[i].startTime + jobs[i].turnAroundTime, timeBuffer);
        printf("%s 周转时间:%d 带权周转时间:%.2f\n", 
               timeBuffer, jobs[i].turnAroundTime, jobs[i].wtTurnAroundTime);
    }
    
    // printf("\n平均周转时间: %.2f 分钟\n", totalTurnAround / jobCount);
    // printf("平均带权周转时间: %.2f\n", totalWtTurnAround / jobCount);
    
    return 0;
}
