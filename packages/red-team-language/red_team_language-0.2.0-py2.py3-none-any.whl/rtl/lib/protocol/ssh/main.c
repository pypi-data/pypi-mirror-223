#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "ssh.h"

int main() {
  unsigned char credential[] =
      "\x06\x00\x08\x00username\x04\x00test\x08\x00password\x08"
      "\x00password\x04\x00type\x08\x00password";
  unsigned char host[] = "\x04\x00\x02\x00ip\x09\x00"
                         "127.0.0.1\x04\x00port\x05\x00"
                         "55555";

  unsigned char command[] = "ls -alh";

  void *connection = protocol_ssh(credential, host);

  if (connection == NULL) {
    printf("Failed to connect\n");
    exit(-1);
  }

  if (0 != execute_remote(connection, command, NULL)) {
    perror("Failure in execution");
  }

  disconnect_remote(connection);
}