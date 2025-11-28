#include <stdio.h>
#include <stdlib.h>

double fcfs_for_disk(int current_track, int requests[], int num_requests) {
    printf("FCFS:\n");
    // 总寻道长度
    double total_seek = 0;
    for (int i = 0; i < num_requests; i++) {
        double seek_distance = abs(current_track - requests[i]);
        total_seek += seek_distance;
        current_track = requests[i];
        printf("visited track:%d\n", current_track);
    }
    return total_seek;
}

int main() {
    // 当前磁头位置
    int current_track = 100;
    // 访问请求序列
    int requests[] = {55, 58, 39, 18, 90, 160, 150, 38, 184};
    // 请求数量
    int num_requests = sizeof(requests) / sizeof(requests[0]);
    
    double fcfs_total_seek = fcfs_for_disk(current_track, requests, num_requests);

    // 计算平均寻道时间
    double avg_seek = fcfs_total_seek / num_requests;
    printf("平均寻道时间: %.1f\n", avg_seek);

    return 0;
}
