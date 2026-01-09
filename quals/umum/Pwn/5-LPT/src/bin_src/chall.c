// gcc chall.c -o chall -lseccomp

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <seccomp.h>
#include <sys/mman.h>

static void init_seccomp(void)   {
    scmp_filter_ctx ctx;
    ctx = seccomp_init(SCMP_ACT_KILL);
    if (!ctx) {
        exit(EXIT_FAILURE);
    }
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(mmap), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(brk), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0);
    if (seccomp_load(ctx) < 0) {
        seccomp_release(ctx);
        exit(EXIT_FAILURE);
    }
}


void init() {
    setvbuf(stdout, NULL, _IONBF, 0);

    FILE *fp = fopen("flag", "r");
    if(fp == NULL) {
        fprintf(stderr, "Error, flag file not found");
        exit(EXIT_FAILURE);
    }

    char flag_buf[0x100];
    fread(flag_buf, 1, 0x100, fp); // free flag?
    memset(flag_buf, 0, 0x100); // nope!
    
    init_seccomp();
    return;
}

void my_read(char *buf, int len) {

    for(int i = 0; i < len-1; i++ ) {
        read(0, buf+i, 1);
        if(buf[i] == '\0' || buf[i] == '\n') {
            buf[i] = '\0';
            break;
        };
    }
}

int main(int argc, char *argv[]) {

    init();

    puts("Give me 5 Life Pro Tips!");

    char buf[0x100];
    for(int i = 0; i < 5; i++)  {
        memset(buf, 0, 0x100);
        printf("Input: ");
        my_read(buf, 0x100);
        printf("Life Pro Tip #%d: ", i+1);
        printf(buf);
        puts("");
    }
    _exit(0);
}
