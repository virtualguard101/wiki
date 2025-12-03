#include <stdio.h>
#include <stdlib.h>


// 升序冒泡排序
void bubble_sort_asc(int arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}

// 降序冒泡排序
void bubble_sort_desc(int arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] < arr[j + 1]) {
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}

// SCAN电梯调度算法
int scan(int current_track, int last_track, int requests[], int num_requests) {
    // 确定移动方向：如果当前磁道大于上次磁道，则向上移动
    int direction = (current_track > last_track) ? 1 : -1; // 1表示向上，-1表示向下
    
    // 分离请求：大于等于当前磁道的和小于当前磁道的
    int up_requests[100], down_requests[100];
    int up_count = 0, down_count = 0;
    
    for (int i = 0; i < num_requests; i++) {
        if (requests[i] >= current_track) {
            up_requests[up_count++] = requests[i];
        } else {
            down_requests[down_count++] = requests[i];
        }
    }
    
    // 排序：向上的请求按升序，向下的请求按降序
    bubble_sort_asc(up_requests, up_count);
    bubble_sort_desc(down_requests, down_count);
    
    int total_movement = 0;
    int prev_track = current_track;
    
    printf("磁头移动顺序：%d", current_track);
    
    // 如果向上移动，先处理向上的请求
    if (direction == 1) {
        // 处理向上的请求
        for (int i = 0; i < up_count; i++) {
            int movement = abs(up_requests[i] - prev_track);
            total_movement += movement;
            printf("、%d", up_requests[i]);
            prev_track = up_requests[i];
        }
        // 然后处理向下的请求
        for (int i = 0; i < down_count; i++) {
            int movement = abs(down_requests[i] - prev_track);
            total_movement += movement;
            printf("、%d", down_requests[i]);
            prev_track = down_requests[i];
        }
    } else {
        // 如果向下移动，先处理向下的请求
        for (int i = 0; i < down_count; i++) {
            int movement = abs(down_requests[i] - prev_track);
            total_movement += movement;
            printf("、%d", down_requests[i]);
            prev_track = down_requests[i];
        }
        // 然后处理向上的请求
        for (int i = 0; i < up_count; i++) {
            int movement = abs(up_requests[i] - prev_track);
            total_movement += movement;
            printf("、%d", up_requests[i]);
            prev_track = up_requests[i];
        }
    }
    
    printf("\n");
    return total_movement;
}

int main() {
    // 磁头上次访问的磁道
    int last_track = 20;
    // 磁头当前位置
    int current_track = 30;
    // 磁盘请求队列
    int requests[] = {38, 6, 37, 100, 14, 124, 65, 67};
    int num_requests = sizeof(requests) / sizeof(requests[0]);
    
    // 执行SCAN算法
    int total_movement = scan(current_track, last_track, requests, num_requests);
    
    printf("经过的磁道数：%d\n", total_movement);
    
    return 0;
}
