#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned u_int;

void get_password(char *str) {
    FILE *fp;
    char *password;
    unsigned int file_size;
    char dst[28];

    fp = fopen("not_the_flag.txt", "r");

    fseek(fp, 0L, SEEK_END);
    file_size = ftell(fp);
    fseek(fp, 0L, SEEK_SET);

    password = (char *) malloc(file_size);

    fscanf(fp, "%s", password);
    printf("%s\n", password );
    fflush(stdout);

    free(password);

    printf(str);
    strcpy(dst, str);
}

u_int rekt_m8(char *str) {
    u_int i, hash, len, tmp;

    hash = 0x12344321;
    len = strlen(str);
    len = len > 7 ? 7 : len;

    for (i = 0; i < len; i++) {
        tmp = hash >> 24;
        hash = hash << 8 | str[i];
        hash ^= tmp;
    }

    return hash;
}

int main() {
    char input[256];

    printf("Fuck yo couch nigga: ");
	fgets(input, 256, stdin);

    if (rekt_m8(input) == 0x4818325b) {
        printf("You good brah\n");
        get_password(input);
    }
    else {
        printf("Check yo self\n");
    }
}
