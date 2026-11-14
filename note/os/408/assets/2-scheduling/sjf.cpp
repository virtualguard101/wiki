#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>
#include <queue>

#define INT_MAX std::numeric_limits<int>::max()

struct Process {
    int id;
    int arrivalTime;
    int burstTime;
    int completionTime;
    int waitingTime;
    int turnaroundTime;
    int remainingTime;
};

// 非抢占式SJF调度算法
void nonPreemptiveSJF(std::vector<Process>& processes) {
    int n = processes.size();
    int currentTime = 0;
    std::vector<bool> completed(n, false);
    
    std::cout << "Non-preemptive SJF scheduling order:\n";
    
    for (int i = 0; i < n; i++) {
        // 找到当前时间已到达且未完成的最短作业
        int shortestIndex = -1;
        int shortestTime = INT_MAX;
        
        for (int j = 0; j < n; j++) {
            if (!completed[j] && 
                processes[j].arrivalTime <= currentTime && 
                processes[j].burstTime < shortestTime) {
                shortestTime = processes[j].burstTime;
                shortestIndex = j;
            }
        }
        
        if (shortestIndex == -1) {
            // 没有进程到达，等待下一个进程到达
            int nextArrival = INT_MAX;
            for (int j = 0; j < n; j++) {
                if (!completed[j]) {
                    nextArrival = std::min(nextArrival, processes[j].arrivalTime);
                }
            }
            currentTime = nextArrival;
            i--; // 重新尝试
            continue;
        }
        
        // 执行选中的进程
        Process& p = processes[shortestIndex];
        p.completionTime = currentTime + p.burstTime;
        p.turnaroundTime = p.completionTime - p.arrivalTime;
        p.waitingTime = p.turnaroundTime - p.burstTime;
        
        std::cout << "Process P" << p.id << " execution time: " << currentTime 
             << " - " << p.completionTime << std::endl;
        
        currentTime = p.completionTime;
        completed[shortestIndex] = true;
    }
}

// 抢占式SJF调度算法
void preemptiveSJF(std::vector<Process>& processes) {
    int n = processes.size();
    int currentTime = 0;
    int completed = 0;
    
    // 初始化剩余时间
    for (auto& p : processes) {
        p.remainingTime = p.burstTime;
    }
    
    std::cout << "Preemptive SJF scheduling order:\n";
    
    while (completed < n) {
        // 找到当前时间已到达且剩余时间最短的进程
        int shortestIndex = -1;
        int shortestTime = INT_MAX;
        
        for (int i = 0; i < n; i++) {
            if (processes[i].remainingTime > 0 && 
                processes[i].arrivalTime <= currentTime && 
                processes[i].remainingTime < shortestTime) {
                shortestTime = processes[i].remainingTime;
                shortestIndex = i;
            }
        }
        
        if (shortestIndex == -1) {
            // 没有进程可执行，跳到下一个到达时间
            int nextArrival = INT_MAX;
            for (int i = 0; i < n; i++) {
                if (processes[i].remainingTime > 0) {
                    nextArrival = std::min(nextArrival, processes[i].arrivalTime);
                }
            }
            currentTime = nextArrival;
            continue;
        }
        
        Process& p = processes[shortestIndex];
        
        // 检查是否有新进程到达并可能抢占
        bool preempted = false;
        for (int i = 0; i < n; i++) {
            if (processes[i].arrivalTime == currentTime + 1 && 
                processes[i].remainingTime < p.remainingTime) {
                // 新进程到达且更短，当前进程被抢占
                std::cout << "Process P" << p.id << " preempted, execution time: " 
                     << currentTime << " - " << currentTime + 1 << std::endl;
                p.remainingTime -= 1;
                currentTime++;
                preempted = true;
                break;
            }
        }
        
        if (!preempted) {
            // 执行到完成
            std::cout << "Process P" << p.id << " execution time: " << currentTime 
                 << " - " << currentTime + p.remainingTime << std::endl;
            
            currentTime += p.remainingTime;
            p.remainingTime = 0;
            p.completionTime = currentTime;
            p.turnaroundTime = p.completionTime - p.arrivalTime;
            p.waitingTime = p.turnaroundTime - p.burstTime;
            completed++;
        }
    }
}

int main() {
    // 测试数据
    std::vector<Process> processes = {
        {1, 0, 8, 0, 0, 0, 0},  // 进程1: 到达时间0, 执行时间8
        {2, 1, 4, 0, 0, 0, 0},  // 进程2: 到达时间1, 执行时间4
        {3, 2, 9, 0, 0, 0, 0},  // 进程3: 到达时间2, 执行时间9
        {4, 3, 5, 0, 0, 0, 0}   // 进程4: 到达时间3, 执行时间5
    };
    
    std::cout << "=== Non-preemptive SJF ===" << std::endl;
    nonPreemptiveSJF(processes);
    
    // 计算并显示统计信息
    float totalWaiting = 0, totalTurnaround = 0;
    for (const auto& p : processes) {
        totalWaiting += p.waitingTime;
        totalTurnaround += p.turnaroundTime;
    }
    
    std::cout << "\nStatistics:" << std::endl;
    std::cout << "Average waiting time: " << totalWaiting / processes.size() << std::endl;
    std::cout << "Average turnaround time: " << totalTurnaround / processes.size() << std::endl;
    
    return 0;
}
