#include <stdio.h>
#include <string.h>


int main() {
    char pass[] = "\x1a\x1c\x19\x0c\x1b\x1a\x0c\x0a\x1b\x0c\x1d\x19\x08\x1a\x1a\x1e\x06\x1b\x0d";
    char input[sizeof(pass)];

    fgets(input, sizeof(input), stdin);

    for (size_t i = 0; i < sizeof(input)-1; i++) {
        input[i] ^= 0x69;
    }

    if (strcmp(input, pass) == 0) {
        puts("YEP :)");
    } else {
        puts("NOPE :(");
    }
}
