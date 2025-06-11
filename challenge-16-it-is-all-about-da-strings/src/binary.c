#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <secret>\n", argv[0]);
        return 1;
    }

    char correct_key[] = "FLAG{w3l1_tH1s_w4S_nOT_th4T_hArD}";
    if (strcmp(argv[1], correct_key) == 0) {
        printf("Correct secret! Access granted!\n");
    }
    else {
        printf("Incorrect secret! Try again.\n");
    }
    return 0;
}
