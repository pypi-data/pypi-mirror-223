#include <assert.h>
#include <inttypes.h>
#include <stdio.h>
#include <string.h>

#include "rtl_common.h"

int main(int argc, char **argv) {
  unsigned char args[] = "\x03\x00\x02\x00-a\x02\x00-l\x02\x00-h";

  unsigned char **buffer = rtl_parse_protocol_argument_buffer(args);

  int i = rtl_get_argument_index(buffer, (unsigned char *)"-l");

  printf("\n-l == arg[%d]\n", i);

  assert(i != -1);
  assert(i == 1);
}