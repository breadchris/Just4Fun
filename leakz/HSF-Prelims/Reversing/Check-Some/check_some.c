
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define BUFFERSIZE 32
#define INTSIZE 32

//flag == flag{u_cant_hash_this_yo_im_too_gewd_fur_u_and_ucant_stwep_me}
//flag matches [a-z{}_]+

typedef unsigned u_int;

u_int entropy[] = {0x1337beef, 0xdeadbeef, 0xcafebabe, 0xdeadbabe, 0x8badf00d, 0xb16b00b5, 0xcafed00d, 0xdeadc0de, 0xdeadfa11, 0xdefec8ed, 0xdeadfeed, 0xfee1dea, 0xfaceb00, 0xfacefee, 0x000ff1c, 0x1234567, 0x743029a, 0xdeed123, 0x0000001, 0x1111111, 0x1111111, 0x1111111, 0x42424242};

u_int checks[] = {0xdde22ab4, 0x7a891cb1, 0xfffe36cc, 0x7fe89124, 0xade54518, 0x8f693026, 0xdbff84fa, 0xbfce5fc6, 0xfefa11f6, 0x55ba5472, 0xbfe0c928, 0x7d92122e, 0x952b4ca4, 0x69dcb5ae, 0xbea74b6b, 0xe6eeb5b7, 0x63f8dfc3, 0x3bc08fcf, 0xf46c0d4d, 0xbf436859, 0x37f8cfe0, 0x3f3dd724, 0xfdead82b, 0xe1f2cefb, 0x5ffdfa88, 0xeb6745db, 0xfbffb982, 0xe7dcb3a1, 0xfe90cf63};

u_int rekt_m8(char *str);
u_int oh_wow(char *str);
u_int get_rekt(char *str);
u_int u_wot(char *str);

u_int (*security[4])(char *) = {
    &rekt_m8,
    &oh_wow,
    &get_rekt,
    &u_wot,
};

void get_password() {
    FILE *fp;
    char *password;
    unsigned int file_size;

    if ((fp = fopen("flag.txt", "r")) == NULL) {
        printf("Need a flag.txt file there dude");
        fflush(stdout);
        exit(1);
    }

    fseek(fp, 0L, SEEK_END);
    file_size = ftell(fp);
    fseek(fp, 0L, SEEK_SET);

    password = (char *) malloc(file_size);

    fscanf(fp, "%s", password);
    printf("%s\n", password );
    fflush(stdout);

    free(password);
}

u_int ror(u_int x, u_int n) {
    return (x << n) | (x >> (INTSIZE - n));
}

u_int rol(u_int x, u_int n) {
    return (x >> (INTSIZE - n)) | (x << n);
}

void add_entropy() {
    u_int i;

    for (i = 0; i < sizeof(entropy) / sizeof(u_int); i++) {
        entropy[i] += 0x11;
    }
}

void add_more_entropy() {
    u_int i;

    for (i = 0; i < sizeof(entropy) / sizeof(u_int); i++) {
        entropy[i] += 0x22;
    }
}

u_int more_entropy(char c) {
    u_int hash, i;

    hash = 0;
    for (i = 0; i < sizeof(entropy) / sizeof(u_int); i++) {
        hash ^= entropy[i] % 2 == 0 ?
            rol(entropy[i], ((u_int) c % 8)):
            ror(entropy[i], ((u_int) c % 8));
    }

    if (hash % 2 == 0) {
        add_entropy();
    }
    else {
        add_more_entropy();
    }

    return hash;
}

u_int rekt_m8(char *str) {
    u_int i, hash, len, tmp;

    hash = more_entropy(str[0]);
    len = strlen(str);
    len = len > 6 ? 6 : len;

    for (i = 0; i < len; i++) {
        tmp = hash >> 24;
        hash *= str[i];
        hash = hash << 8 | str[i];
        hash ^= tmp;
    }

    return hash;
}

u_int oh_wow(char *str) {
    u_int i, hash, len, tmp;

    hash = more_entropy(str[0]);
    len = strlen(str);
    len = len > 6 ? 6 : len;

    for (i = 0; i < len; i++) {
        hash += str[i];
    }

    return hash;
}

u_int get_rekt(char *str) {
    u_int i, len, tmp;
    int hash;

    hash = more_entropy(str[0]);
    len = strlen(str);
    len = len > 6 ? 6 : len;

    for (i = 0; i < len; i++) {
        hash += ((u_int) str[i]) * 2;
    }

    return (u_int) hash;
}

u_int u_wot(char *str) {
    u_int i, hash, len, tmp;

    hash = more_entropy(str[0]);
    len = strlen(str);
    len = len > 6 ? 6 : len;

    for (i = 0; i < len; i++) {
        hash ^= hash << 8 | str[i];
    }

    return hash;
}

int main() {
    u_int i, len, idx, func_bounds, check, checks_passed;
    char password[BUFFERSIZE];

    memset(password, '\0', BUFFERSIZE);
    fgets(password, BUFFERSIZE - 1, stdin);

    len = strlen(password);

    if (password[len - 1] == '\n')
        password[len - 1] = '\0';

    func_bounds = ( sizeof(security) / sizeof(void *) );
    checks_passed = 0;

    for (i = 0; i < len; i++) {
        idx = password[i] % func_bounds;

        if (idx + i >= len - 1) break;

        check = (security[idx](password + i) << 21) | security[idx](password + i + idx);

        if (i % 2 == 0) {
            if (check != checks[i / 2]) {
                printf("Nope :c");
                fflush(stdout);
                exit(1);
            }
            else {
                checks_passed += 1;
            }
        }
    }

    if (checks_passed == sizeof(checks) / sizeof(u_int)) {
        printf("AHH Yis :3\n");
        fflush(stdout);
        get_password();
    } else {
        printf("Nope!");
        fflush(stdout);
    }
}
