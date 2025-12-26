#include <stdio.h>

#define FRAME_SIZE 3

typedef struct{
    int data[FRAME_SIZE];
    int top;
    int count;
} Stack;

int find(int arr[], int size, int value){
    for(int i = 0; i < size; i++) if(arr[i] == value) return i;
    return -1;
}

void init_stack(Stack *s){
    s->top = -1;
    s->count = 0;
}

void push(Stack *s, int value){//入栈操作
    if(s->count < FRAME_SIZE){
        s->data[++s->top] = value;
        s->count++;
    }
    else{
        for(int i = 0; i < s->count - 1; i++) s->data[i] = s->data[i + 1];
        s->data[s->top] = value;
    }
}

void move_to_top(Stack *s, int index){//更新
    int value = s->data[index];
    for(int i = index; i < s->count - 1; i++) s->data[i] = s->data[i + 1];
    s->data[s->top] = value;
}

void printmemory(int memory[], int size){
    for(int i = 0; i < size; i++){
        if (memory[i] == -1) printf("x ");
        else printf("%d ", memory[i]);
    }
    printf("\n");
}

void handle_page(Stack *s, int *memory, int page, int *f){
    int rds = find(memory, FRAME_SIZE, page);//内存中的位置
    int sds = find(s->data, s->count, page);//栈中的位置

    if(rds == -1){
        (*f)++;
        if (s->count < FRAME_SIZE)  memory[s->count] = page;
        else{
            int lruPage = s->data[0];
            int lruIdx = find(memory, FRAME_SIZE, lruPage);
            memory[lruIdx] = page;
        }
        push(s, page);
    }
    else move_to_top(s, sds);
}

void lru_do(int ref[], int ref_len){
    int memory[FRAME_SIZE] = {-1, -1, -1};
    Stack stack;
    int f = 0;

    init_stack(&stack);
    
    for(int i = 0; i < ref_len; i++){
        int page = ref[i];
        handle_page(&stack, memory, page, &f);
        printmemory(memory, FRAME_SIZE);
    }

    printf("f=%.1f\n", (float)f / ref_len);
}

int main(){
    int ref[] = {7, 0, 1, 2, 0, 3, 0, 4, 2, 3};
    int ref_len = sizeof(ref) / sizeof(ref[0]);
    lru_do(ref, ref_len);
    return 0;
}
