// This program is broken. Pointers are weird

#include <stdio.h>

int main() {
    int x = 0;
    int y = 0;
    puts("hi!");
    scanf("%d", x);
    scanf("%d", y);
    float z = x / y;
    printf("%.2f\n", z);
}
