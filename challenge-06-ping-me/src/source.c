#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <regex.h>

#define MAX_COMMAND_LEN 256

void init()
{
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stderr, 0, 2, 0);
}

int valid_ip(const char *ip) {
    regex_t regex;
    int ret;

    const char *pattern = "^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$";

    ret = regcomp(&regex, pattern, REG_EXTENDED);
    if (ret) {
        fprintf(stderr, "Could not compile regex\n");
        exit(1);
    }

    ret = regexec(&regex, ip, 0, NULL, 0);
    regfree(&regex);

    return ret == 0;
}

int main() {

    init();

    char ip[100];
    printf("Enter IP Address: ");
    if (fgets(ip, sizeof(ip), stdin) == NULL) {
        printf("Error reading input.\n");
        return 1;
    }

    
    size_t len = strlen(ip);
    if (len > 0 && ip[len - 1] == '\n') {
        ip[len - 1] = '\0';
    }

    if (!valid_ip(ip)) {
        printf("Invalid IP address format. Exiting.\n");
        return 1;
    }

    char command[MAX_COMMAND_LEN];
    snprintf(command, sizeof(command), "ping -c 4 %s", ip);

    printf("Executing command: %s\n", command);

    int status = system(command);

    if (status == 0) {
        printf("Ping successful.\n");
        
        char additional_args[100];
        printf("Do you want anything else to add? Enter additional arguments: ");
        if (fgets(additional_args, sizeof(additional_args), stdin) == NULL) {
            printf("Error reading input.\n");
            return 1;
        }

        size_t len = strlen(additional_args);
        if (len > 0 && additional_args[len - 1] == '\n') {
            additional_args[len - 1] = '\0';
        }

        snprintf(command, sizeof(command), "ping -c 4 %s %s", ip, additional_args);
        printf("Executing command: %s\n", command);

        status = system(command);

        if (status == 0) {
            printf("\nCommand successful.\n");
        } else {
            printf("\nCommand failed.\n");
        }
    } else {
        printf("Ping failed.\n");
    }

    return 0;
}