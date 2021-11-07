#include <stdint.h>
#include <stdio.h>

void __bx_print_int(int64_t x) { printf("%lld\n", x); }
void __bx_print_bool(int64_t b) { printf("%s\n", b ? "true" : "false"); }