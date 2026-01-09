// gcc baby_rop.c -o baby_rop -fno-stack-protector

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
}

int main(int argc, char *argv[]) {

    init();

    char buf[0x20];

    puts("Baby ROP");
    read(0, buf, 0x200); // oops
    
    printf("Heres your leak! %p\n", printf);
    puts("Eh... kebalik ya");

    return 0;
}
