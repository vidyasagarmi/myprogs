#include <stdio.h>
struct test {
    unsigned long int Size:48;
    unsigned long int ReqSize:48;
    unsigned int Alloced:1;
    unsigned int Free:1;
    unsigned int Pad:6;
    unsigned int Magic:24;
}__attribute__((packed));

int main() {
    printf("%d %d\n", sizeof(unsigned long int), sizeof(unsigned int));
    printf("%d\n", sizeof(struct test));
}
