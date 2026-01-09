// gcc forgotten_flag.c -o forgotten_flag -no-pie

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

char flag_buf[0x100]; // flag is saved here, leak it!

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);

    FILE *fp = fopen("flag.txt", "r");
    if(fp == NULL) {
        fprintf(stderr, "Error, flag file not found");
        exit(EXIT_FAILURE);
    }

    fread(flag_buf, 1, 0x100, fp);
    return;
}

int main(int argc, char *argv[]) {

    init();

    char buf[0x100];

    puts("Forgotten Flag");
    puts("Leak my flag in bss");
    printf("Input: ");

    fgets(buf, 0x100, stdin);
    printf(buf);

    puts("Did you leak it?");

    return 0;
}
