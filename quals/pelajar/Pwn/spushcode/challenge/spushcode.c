// gcc spushcode.c -o spushcode

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>

char *spushcode;

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);

    spushcode = mmap(NULL, 0x1000, 7, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if(spushcode == MAP_FAILED) {
        fprintf(stderr, "Error, contact admin\n");
        exit(1);
    }
    return;
}

int check_spushcode(char *spushcode, int num_read) {
    for(int i = 0; i < num_read; i++) {
        if(spushcode[i] >= 'P' && spushcode[i] <= '_') continue; // any single char push or pop is allowed
        if(spushcode[i] == '\x0f' && spushcode[i+1] == '\x05') { i++; continue; } // syscall is allowed
        else return 0; // nothing else is allowed
    }
    return 1;
}

int main(int argc, char *argv[]) {

    init();

    printf("Enter your shellcode: ");
    int num_read = read(0, spushcode, 0x1000);
    if(spushcode[num_read-1] == '\n') spushcode[num_read-1] = '\0';

    if(!check_spushcode(spushcode, num_read-1)) {
        fprintf(stderr, "Invalid spushcode\n");
        exit(1);
    }

    ((void (*)())spushcode)();

    return 0;
}
