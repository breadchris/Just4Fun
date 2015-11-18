#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>

static uint64_t seed;

uint64_t next_cypher(uint64_t range)
{
    float factor = ((float) range) / RAND_MAX;
    uint64_t scaled = (seed ^ seed << 1 | 1) * factor;

    seed = scaled / factor;

    return scaled;
}

uint64_t _hash(char *str)
{
    uint64_t h, a, i, len;
    a = 33;
    h = 5381;
    len = strlen(str);
    for (i = 0; i < len; ++i) {
        h += (h * a) + str[i];
    }
    return h;
}

int main(int argc, char **argv) {
    int i = 0;
    int p, c;
    printf("                                       .;;.\n"
           "                ____________________. ;;  ;;\n"
           "   ,;;;;;.     /                   /|  `. ;;\n"
           " .;`    `;;   /   NECRONOMICON    / ;`.;..;`\n"
           " ;; ,;;. ;;  /                   / /    ``\n"
           " ;; ` ;; ;;./                   / /.;;.\n"
           " `;;;;`   `/    (c) 20XX       / /.`  ;;\n"
           "          /   HYPERACTIVE     / /  .` ;;\n"
           "  .;;.   /                   / /   `;;`\n"
           " ;;  ` ./    52.70.20.87    / /`;.\n"
           " ;; .;`/                   / /.  ;;\n"
           "  `;; ;___________________/ / `;;`\n"
           "      |____________________/\n");

    if (argc < 4) {
        printf("Usage: %s key infile outfile\n", argv[0]);
        exit(0);
    }
    seed = _hash(argv[1]);
    FILE* input  = fopen(argv[2], "rb");
    FILE* output = fopen(argv[3], "wb");
    if  (!input || !output) {
        printf("Error!\n");
        return 1;
    }
    printf("Working...\n");
    while ((p = fgetc(input)) != EOF) {
        c = (p ^ (next_cypher(UINT32_MAX) & 0xFF));
        fputc(c, output);
    }
    printf("Done!\n");
    fclose(input);
    fclose(output);
    return 0;
}
