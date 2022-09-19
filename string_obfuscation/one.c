#include <stdio.h>
#include <string.h>

char pass[] = "supersecretpassword";

int main() {
    char input[sizeof(pass)];

    fgets(input, sizeof(input), stdin);

    if (strcmp(input, pass) == 0) {
        puts("YEP :)");
    } else {
        puts("NOPE :(");
    }
}
