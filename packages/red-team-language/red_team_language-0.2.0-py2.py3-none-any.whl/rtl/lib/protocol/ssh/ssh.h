#ifndef _RTL_PROTOCOL_SHELL_REMOTE_H
#define _RTL_PROTOCOL_SHELL_REMOTE_H

#include "./libssh2/include/libssh2.h"
#include <inttypes.h>

#define DEBUG 1

typedef struct _RTL_REMOTE_CONNECTION {

  libssh2_socket_t socket;
  LIBSSH2_SESSION *session;
} RTL_REMOTE_CONNECTION;

extern void *protocol_ssh(unsigned char *credential, unsigned char *host);
extern int execute_remote(void *connection, unsigned char *command,
                          unsigned char *envp);
extern void disconnect_remote(void *connection);

#endif