#include <stdio.h>
#include <stdbool.h>

#define MAX_PAGES 25
#define PHYSICAL_BLOCKS 3

// 查找页面在内存中的位置，返回-1表示不在内存中
int findPage(int memory[], int page, int size) {
    for (int i = 0; i < size; i++) {
        if (memory[i] == page) {
            return i;
        }
    }
    return -1;
}

// 查找页面在未来访问序列中的下一次访问位置
int findNextAccess(int sequence[], int start, int length, int page) {
    for (int i = start; i < length; i++) {
        if (sequence[i] == page) {
            return i;
        }
    }
    return length; // 如果未来不再访问，返回序列长度
}

// OPT算法: 选择未来最长时间不会被访问的页面进行置换
int selectVictim(int memory[], int sequence[], int currentIndex, int seqLength, int blockCount) {
    int victimIndex = 0;
    int maxNextAccess = -1;
    
    for (int i = 0; i < blockCount; i++) {
        int nextAccess = findNextAccess(sequence, currentIndex + 1, seqLength, memory[i]);
        if (nextAccess > maxNextAccess) {
            maxNextAccess = nextAccess;
            victimIndex = i;
        }
    }
    return victimIndex;
}

int main() {
    // 页面访问序列
    // int sequence[] = {1, 2, 4, 2, 6, 2, 1, 5, 6, 1};
    int sequence[] = {6, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 6, 1, 0};
    int seqLength = sizeof(sequence) / sizeof(sequence[0]);
    
    // 初始化物理块，初始状态：1, 2, 3
    int memory[PHYSICAL_BLOCKS] = {1, 2, 3};
    int blockCount = PHYSICAL_BLOCKS;
    
    // 记录每个页面是否已经被访问过（用于判断初始状态页面的首次访问）
    bool pageAccessed[8] = {false}; // 页面编号1-7
    
    // 记录缺页情况
    bool pageFault[MAX_PAGES];
    int faultCount = 0;
    
    for (int i = 0; i < seqLength; i++) {
        printf("%d", sequence[i]);
        if (i < seqLength - 1) {
            printf(", ");
        }
    }
    printf("\n");
    
    // 模拟页面访问
    for (int i = 0; i < seqLength; i++) {
        int page = sequence[i];
        int pos = findPage(memory, page, blockCount);
        
        // 如果页面不在内存中，或者页面在内存中但这是第一次访问（初始状态的页面）
        if (pos == -1 || !pageAccessed[page]) {
            // 缺页
            pageFault[i] = true;
            faultCount++;
            
            if (pos == -1) {
                // 页面不在内存中，需要置换
                // 查找空闲块
                bool hasEmpty = false;
                for (int j = 0; j < blockCount; j++) {
                    if (memory[j] == -1) {
                        memory[j] = page;
                        hasEmpty = true;
                        break;
                    }
                }
                
                if (!hasEmpty) {
                    // 没有空闲块，使用OPT算法选择置换页面
                    int victimIndex = selectVictim(memory, sequence, i, seqLength, blockCount);
                    memory[victimIndex] = page;
                }
            }
            
            // 标记页面已被访问
            pageAccessed[page] = true;
        } else {
            // 页面已在内存中且之前已访问过，不缺页
            pageFault[i] = false;
        }
    }
    
    // 输出缺页情况
    for (int i = 0; i < seqLength; i++) {
        printf("%s", pageFault[i] ? "Y" : "N");
        if (i < seqLength - 1) {
            printf(", ");
        }
    }
    printf("\n");
    
    // 计算并输出缺页率
    double faultRate = (double)faultCount / seqLength;
    printf("OPT: f=%.2f\n", faultRate);
    
    return 0;
}
