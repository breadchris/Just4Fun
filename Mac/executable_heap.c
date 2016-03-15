
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

int main() {

    void *block = malloc(1024 * 1024 * 1337);
    printf("%d\n", getpid());
    while (1) {
    }
}
