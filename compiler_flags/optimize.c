// Throw the following in godbolt and check the difference in compiler output with no flags, -O, and -O3

#include <stdio.h>

int main () {
    int n = 100;
    int sum = 0;
    for (int i = 1; i <= n; i++) {
        sum += i;
    }
    printf("%d", sum);
}
