#include <stdlib.h>
#include <stdio.h>

typedef struct test_s test_t;
extern void print_struct(test_t *s);
int main() {
    test_t s;
    s.i = 100;
    print_struct(&s);
}
