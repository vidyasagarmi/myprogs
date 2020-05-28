#include <stdlib.h>
#include <stdio.h>

typedef struct test_s{
    int i;
}test_t;

void print_struct(test_t *s) {
    printf("val: %d\n", s->i);
}
