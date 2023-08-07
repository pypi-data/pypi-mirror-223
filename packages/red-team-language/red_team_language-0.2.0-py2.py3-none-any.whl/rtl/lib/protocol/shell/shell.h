#ifndef _RTL_PROTOCOL_SHELL_H
#define _RTL_PROTOCOL_SHELL_H

#include <inttypes.h>

typedef enum _RTL_PROTOCOL_SHELL_METHODS {
  RTL_PROTOCOL_SHELL_METHOD_MEMFD,
  RTL_PROTOCOL_SHELL_METHOD_TMPFS,
} RTL_PROTOCOL_SHELL_METHODS;

extern int protocol_shell(uint32_t, unsigned char *, uint32_t, unsigned char *,
                          unsigned char *);

#endif