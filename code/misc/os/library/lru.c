#include <stdio.h>

#define MAX_FRAMES 3
#define REF_LEN 10

void lru_page_replacement() {
    int ref[] = {7, 0, 1, 2, 0, 3, 0, 4, 2, 3};
    int frames[MAX_FRAMES] = {-1, -1, -1}; //展示存放
    int stack[MAX_FRAMES]; //模拟栈
    int stack_size = 0;
    int f = 0; //缺页数
    
    for(int i = 0; i < REF_LEN; i++){
        int page = ref[i];//当前页面
        int found = 0;
        int pos = -1;
        
        for(int j = 0; j < stack_size; j++){//检查当前页面是否在内存中
            if(page == stack[j]){
                found = 1;
                pos = j;
                break;
            }
        }
        if(found){
            for (int j = pos; j < stack_size - 1; j++) stack[j] = stack[j + 1];//更新位置
            stack[stack_size - 1] = page;
        }else{ // Frame Fault
            f++;
            if(stack_size < MAX_FRAMES){//未满
                stack[stack_size++] = page;

                for (int j = 0; j < MAX_FRAMES; j++){
                    if (frames[j] == -1) {
                        frames[j] = page;
                        break;
                    }
                }
            }else{
                int lru_page = stack[0];
                for(int j = 0; j < stack_size - 1; j++) stack[j] = stack[j + 1];//满了就替换
                stack[stack_size - 1] = page;
                
                for(int j = 0; j < MAX_FRAMES; j++){
                    if(frames[j] == lru_page){
                        frames[j] = page;
                        break;
                    }
                }
            }
        }

        for(int j = 0; j < MAX_FRAMES; j++){
            if(frames[j] == -1) printf("x ");
            else printf("%d ", frames[j]);
        }

        printf("\n");
    }

    printf("f=%.1f\n", (float)f / REF_LEN);
}

int main() {
    lru_page_replacement();
    return 0;
}
