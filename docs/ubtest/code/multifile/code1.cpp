#include<cstdio>

extern int fibonacci(int n);

int main() {
    int n;
    scanf("%d", &n);
    for (int i = 0; i < n; i++) {
        printf("%d\n", fibonacci(i));
    }
    return 0;
}