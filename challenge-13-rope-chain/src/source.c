#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <string.h>

void banner() {
    printf("====================================\n");
    printf("   Welcome to the Rope-Store \n");
    printf("====================================\n");
    printf(" Can you untangle the ropes?\n");
    printf("====================================\n");
    printf(" Rules:\n");
    printf(" 1. Keep the ropes short!\n");
    printf(" 2. Keep your input under control.\n");
    printf(" 3. Timeout is 60 seconds.\n");
    printf("====================================\n\n");
}

// --------------------------------------------------- SETUP

void buffering() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void kill_on_timeout(int sig) {
    if (sig == SIGALRM) {
        exit(0);
    }
}

void alarm_signal() {
    signal(SIGALRM, kill_on_timeout);
    alarm(60);
}

int main(void) {
    char buffer[32];

    buffering();
    alarm_signal();

    banner();

    printf("> ");
    fflush(stdout);
    fgets(buffer, 256, stdin);

    printf("\nThank you for visiting..\n");

    return 0;
}
