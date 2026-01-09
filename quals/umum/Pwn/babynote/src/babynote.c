/*
 * BabyNote - ASIS CTF 2025 Final
 * Compile: gcc -o babynote babynote.c
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <signal.h>
#include <time.h>
#include <errno.h>
#include <limits.h>

#define MAX_NOTES 16
#define MAX_SIZE 0x100
#define TIMEOUT 120

char g_path[64];
int g_fd = -1;

typedef struct {
    uint32_t sz;
    uint32_t used;
} __attribute__((packed)) NoteInfo;

typedef struct {
    char* data;
    uint64_t sz;
} Note;

Note g_notes[MAX_NOTES];

void alarm_handler(int sig) {
    puts("\n[!] Time's up!");
    _exit(0);
}

void init() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    
    signal(SIGALRM, alarm_handler);
    alarm(TIMEOUT);
    
    srand(time(NULL));
    snprintf(g_path, sizeof(g_path), "/tmp/.n%04d", rand() % 10000);
    
    g_fd = open(g_path, O_RDWR | O_CREAT, 0666);
    if (g_fd < 0) {
        _exit(1);
    }
    
    struct stat st;
    fstat(g_fd, &st);
    if (st.st_size == 0) {
        NoteInfo empty = {0, 0};
        for (int i = 0; i < MAX_NOTES; i++) {
            write(g_fd, &empty, sizeof(NoteInfo));
        }
    }
}

uint64_t get_uint() {
    char buf[32];
    if (fgets(buf, sizeof(buf), stdin) == NULL) {
        _exit(0);
    }
    
    char* endptr;
    errno = 0;
    unsigned long val = strtoul(buf, &endptr, 10);
    
    if (errno != 0 || endptr == buf) {
        return UINT64_MAX;
    }
    
    return (uint64_t)val;
}

void get_str(char* buf, uint64_t len) {
    if (len == 0) return;
    
    uint64_t i = 0;
    char c;
    while (i < len - 1) {
        if (read(STDIN_FILENO, &c, 1) <= 0) break;
        if (c == '\n') break;
        buf[i++] = c;
    }
    buf[i] = '\0';
}

int check_note(uint64_t idx) {
    if (idx >= MAX_NOTES) {
        return -1;
    }
    
    if (g_notes[idx].data == NULL) {
        return -1;
    }
    
    NoteInfo info;
    lseek(g_fd, idx * sizeof(NoteInfo), SEEK_SET);
    read(g_fd, &info, sizeof(NoteInfo));
    
    if (!info.used) {
        return -1;
    }
    
    g_notes[idx].sz = info.sz;
    
    if (g_notes[idx].sz == 0 || g_notes[idx].sz > MAX_SIZE) {
        return -1;
    }
    
    return 0;
}

void add() {
    int slot = -1;
    for (int i = 0; i < MAX_NOTES; i++) {
        if (g_notes[i].data == NULL) {
            slot = i;
            break;
        }
    }
    
    if (slot == -1) {
        puts("[-] Full");
        return;
    }
    
    printf("Size: ");
    uint64_t sz = get_uint();
    
    if (sz == 0 || sz > MAX_SIZE) {
        puts("[-] Invalid");
        return;
    }
    
    char* ptr = (char*)malloc(sz);
    if (ptr == NULL) {
        puts("[-] Failed");
        return;
    }
    
    memset(ptr, 0, sz);
    
    g_notes[slot].data = ptr;
    g_notes[slot].sz = sz;
    
    NoteInfo info;
    info.sz = (uint32_t)sz;
    info.used = 1;
    lseek(g_fd, slot * sizeof(NoteInfo), SEEK_SET);
    write(g_fd, &info, sizeof(NoteInfo));
    
    printf("[+] Note %d\n", slot);
}

void edit() {
    printf("Index: ");
    uint64_t idx = get_uint();
    
    if (check_note(idx) != 0) {
        puts("[-] Error");
        return;
    }
    
    printf("Data: ");
    get_str(g_notes[idx].data, g_notes[idx].sz);
    
    puts("[+] Done");
}

void view() {
    printf("Index: ");
    uint64_t idx = get_uint();
    
    if (idx >= MAX_NOTES) {
        puts("[-] Invalid");
        return;
    }
    
    NoteInfo info;
    lseek(g_fd, idx * sizeof(NoteInfo), SEEK_SET);
    read(g_fd, &info, sizeof(NoteInfo));
    
    if (!info.used) {
        puts("[-] Empty");
        return;
    }
    
    if (g_notes[idx].data == NULL) {
        puts("[-] Error");
        return;
    }
    
    printf("Content: %s\n", g_notes[idx].data);
}

void del() {
    printf("Index: ");
    uint64_t idx = get_uint();
    
    if (idx >= MAX_NOTES) {
        puts("[-] Invalid");
        return;
    }
    
    NoteInfo info;
    lseek(g_fd, idx * sizeof(NoteInfo), SEEK_SET);
    read(g_fd, &info, sizeof(NoteInfo));
    
    if (!info.used) {
        puts("[-] Empty");
        return;
    }
    
    if (g_notes[idx].data == NULL) {
        puts("[-] Error");
        return;
    }
    
    free(g_notes[idx].data);
    g_notes[idx].data = NULL;
    g_notes[idx].sz = 0;
    
    info.sz = 0;
    info.used = 0;
    lseek(g_fd, idx * sizeof(NoteInfo), SEEK_SET);
    write(g_fd, &info, sizeof(NoteInfo));
    
    puts("[+] Deleted");
}

void menu() {
    puts("\n=== BabyNote ===");
    puts("1. Add");
    puts("2. Edit");
    puts("3. View");
    puts("4. Delete");
    puts("5. Exit");
    printf(">> ");
}

int main() {
    init();
    
    puts("Welcome to BabyNote!");
    
    while (1) {
        menu();
        uint64_t c = get_uint();
        
        switch (c) {
            case 1: add(); break;
            case 2: edit(); break;
            case 3: view(); break;
            case 4: del(); break;
            case 5: puts("Bye!"); return 0;
            default: puts("?");
        }
    }
    
    return 0;
}
