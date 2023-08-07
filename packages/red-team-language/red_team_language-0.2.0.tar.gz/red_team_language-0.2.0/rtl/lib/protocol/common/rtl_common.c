#define _GNU_SOURCE /* See feature_test_macros(7) */
#include <errno.h>
#include <fcntl.h>
#include <inttypes.h>
#include <linux/memfd.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/wait.h>
#include <unistd.h>

#include "rtl_common.h"

int rtl_get_argument_index(unsigned char **argv, unsigned char *key) {
  int i = 0;

#ifdef DEBUG
  printf("Argument Buffer to Search for key |%s|: \n", key);
  do {
    printf("\targ[%d] = |||%s|||\n", i, argv[i]);
  } while (argv[i++] != NULL);
  i = 0;
#endif

  do {
    if (argv[i] == NULL) {
      break;
    }

    if (strncmp((const char *)key, (const char *)argv[i],
                fmin(strlen((const char *)key),
                     strlen((const char *)argv[i]))) == 0) {
      return i;
    }
  } while (argv[i++] != NULL);

  return -1;
}

unsigned char **rtl_parse_protocol_argument_buffer(unsigned char *buf) {

  uint16_t argc = 0;

  if (buf != NULL) {
    argc = (uint16_t) * (buf);
  }

  uint16_t offset = sizeof(uint16_t);

  unsigned char **argv = calloc(argc + 1, sizeof(unsigned char *));

  for (uint16_t i = 0; i < argc; i++) {
    uint16_t arg_sz = (uint16_t) * (buf + offset);
    offset += sizeof(uint16_t);

    argv[i] = calloc(arg_sz + 1, sizeof(unsigned char));

    memcpy(argv[i], buf + offset, arg_sz);

    offset += arg_sz;
  }

  argv[argc] = NULL;

#ifdef DEBUG
  printf("Argument Buffer: \n");
  int i = 0;
  do {
    printf("\targ[%d] = |||%s|||\n", i, argv[i]);
  } while (argv[i++] != NULL);
#endif

  return argv;
}
