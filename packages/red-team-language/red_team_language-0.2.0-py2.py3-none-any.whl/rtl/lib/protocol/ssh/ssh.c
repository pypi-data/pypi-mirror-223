// #include "libssh2_setup.h"
#include "./libssh2/include/libssh2.h"

// for now...
#define HAVE_SYS_SOCKET_H 1
#define HAVE_UNISTD_H 1
#define HAVE_ARPA_INET_H 1

#ifdef HAVE_SYS_SOCKET_H
#include <sys/socket.h>
#include <sys/types.h> /* See NOTES */
#endif
#ifdef HAVE_UNISTD_H
#include <unistd.h>
#endif
#ifdef HAVE_NETINET_IN_H
#include <netinet/in.h>
#endif
#ifdef HAVE_ARPA_INET_H
#include <arpa/inet.h>
#endif

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "../common/rtl_common.h"
#include "ssh.h"

const unsigned char rtl_credential_type[] = "type\x00";
const unsigned char rtl_credential_username[] = "username\x00";
const unsigned char rtl_credential_password[] = "password\x00";
const unsigned char rtl_host_ip[] = "ip\x00";
const unsigned char rtl_host_port[] = "port\x00";

static int waitsocket(libssh2_socket_t socket_fd, LIBSSH2_SESSION *session) {
  struct timeval timeout;
  int rc;
  fd_set fd;
  fd_set *writefd = NULL;
  fd_set *readfd = NULL;
  int dir;

  timeout.tv_sec = 10;
  timeout.tv_usec = 0;

  FD_ZERO(&fd);

  FD_SET(socket_fd, &fd);

  /* now make sure we wait in the correct direction */
  dir = libssh2_session_block_directions(session);

  if (dir & LIBSSH2_SESSION_BLOCK_INBOUND)
    readfd = &fd;

  if (dir & LIBSSH2_SESSION_BLOCK_OUTBOUND)
    writefd = &fd;

  rc = select((int)(socket_fd + 1), readfd, writefd, NULL, &timeout);

  return rc;
}

extern void *protocol_ssh(unsigned char *r, unsigned char *h) {
  unsigned char **credential = rtl_parse_protocol_argument_buffer(r);
  unsigned char **host = rtl_parse_protocol_argument_buffer(h);
  RTL_REMOTE_CONNECTION *connection =
      (RTL_REMOTE_CONNECTION *)calloc(1, sizeof(RTL_REMOTE_CONNECTION));
  uint32_t hostaddr;
  struct sockaddr_in sin;
  const char *fingerprint;
  int rc;
  LIBSSH2_SESSION *session = NULL;

#ifdef WIN32
  WSADATA wsadata;

  rc = WSAStartup(MAKEWORD(2, 0), &wsadata);
  if (rc) {
    fprintf(stderr, "WSAStartup failed with error: %d\n", rc);
    return NULL;
  }
#endif

  int i =
      rtl_get_argument_index(credential, (unsigned char *)rtl_credential_type);

  if (i == -1) {
    perror("Failed to locate type");
    exit(-1);
  }

  unsigned char *type = credential[i + 1];
  unsigned int credential_type =
      strncmp("password", (const char *)type,
              strlen((const char *)type)) == 0; // fmin?...

  i = rtl_get_argument_index(credential,
                             (unsigned char *)rtl_credential_username);

  if (i == -1) {
    perror("Failed to locate username");
    exit(-1);
  }

  unsigned char *username = credential[i + 1];

  i = rtl_get_argument_index(credential,
                             (unsigned char *)rtl_credential_password);

  if (i == -1) {
    perror("Failed to locate password");
    exit(-1);
  }

  unsigned char *password = credential[i + 1];

  i = rtl_get_argument_index(host, (unsigned char *)rtl_host_ip);

  if (i == -1) {
    perror("Failed to locate ip");
    exit(-1);
  }

  unsigned char *hostname = host[i + 1];

  i = rtl_get_argument_index(host, (unsigned char *)rtl_host_port);
  unsigned int port = 22;

  if (i == -1) {
    perror("Failed to locate port - defaulting to port 22");
  }

  port = atoi((const char *)host[i + 1]);

#ifdef DEBUG
  printf("Connecting to: %s:%s@%s\n\n", username, password, hostname);
#endif

  rc = libssh2_init(0);
  if (rc) {
    fprintf(stderr, "libssh2 initialization failed (%d)\n", rc);
    return NULL;
  }

  hostaddr = inet_addr((const char *)hostname);

  /* Ultra basic "connect to port on localhost".  Your code is
   * responsible for creating the socket establishing the connection
   */
  connection->socket = socket(AF_INET, SOCK_STREAM, 0);
  if (connection->socket == LIBSSH2_INVALID_SOCKET) {
    fprintf(stderr, "failed to create socket!\n");
    goto shutdown;
  }

  sin.sin_family = AF_INET;
  sin.sin_port = htons(port);
  sin.sin_addr.s_addr = hostaddr;
  if (connect(connection->socket, (struct sockaddr *)(&sin),
              sizeof(struct sockaddr_in))) {
    fprintf(stderr, "failed to connect!\n");
    goto shutdown;
  }

  /* Create a session instance */
  session = libssh2_session_init();
  if (!session) {
    fprintf(stderr, "Could not initialize SSH session!\n");
    goto shutdown;
  }

  /* tell libssh2 we want it all done non-blocking */
  libssh2_session_set_blocking(session, 0);

  /* ... start it up. This will trade welcome banners, exchange keys,
   * and setup crypto, compression, and MAC layers
   */
  while ((rc = libssh2_session_handshake(session, connection->socket)) ==
         LIBSSH2_ERROR_EAGAIN)
    ;

  if (rc) {
    fprintf(stderr, "Failure establishing SSH session: %d\n", rc);
    goto shutdown;
  }
  // TODO: fingerprint check?
  fingerprint = libssh2_hostkey_hash(session, LIBSSH2_HOSTKEY_HASH_SHA256);
#ifdef DEBUG
  fprintf(stderr, "Fingerprint: ");
  for (int i = 0; i < 20; i++)
    fprintf(stderr, "%02X ", (unsigned char)fingerprint[i]);
  fprintf(stderr, "\n");
#endif

  if (credential_type == 1) {
    /* We could authenticate via password */
    while ((rc = libssh2_userauth_password(session, (const char *)username,
                                           (const char *)password)) ==
           LIBSSH2_ERROR_EAGAIN)
      ;
    if (rc) {
      fprintf(stderr, "Authentication by password failed!\n");
      goto shutdown;
    }
  }
  // not yet...
  // else {
  //     /* Or by public key */
  //     while((rc = libssh2_userauth_publickey_fromfile(session, username,
  //                                                     pubkey, privkey,
  //                                                     credential)) ==
  //           LIBSSH2_ERROR_EAGAIN);
  //     if(rc) {
  //         fprintf(stderr, "Authentication by public key failed!\n");
  //         goto shutdown;
  //     }
  // }

#if 0
    libssh2_trace(session, ~0);
#endif

  goto success;

shutdown:

  if (connection) {
    free(connection);
    connection = NULL;
  }

  if (session) {
    libssh2_session_disconnect(session, "Normal Shutdown");
    libssh2_session_free(session);
  }

  if (connection->socket != LIBSSH2_INVALID_SOCKET) {
    shutdown(connection->socket, 2);
#ifdef WIN32
    closesocket(connection->socket);
#else
    close(connection->socket);
#endif
  }

  fprintf(stderr, "all done\n");

  libssh2_exit();

  return NULL;

success:

  connection->session = session;

  return (void *)connection;
}

extern int execute_remote(void *c, unsigned char command[], unsigned char *e) {
  unsigned char **envp = rtl_parse_protocol_argument_buffer(e);
  int rc;
  RTL_REMOTE_CONNECTION *connection = (RTL_REMOTE_CONNECTION *)c;
  LIBSSH2_SESSION *session = connection->session;
  libssh2_socket_t sock = connection->socket;
  LIBSSH2_CHANNEL *channel;
  int exitcode;
  char *exitsignal = (char *)"none";
  ssize_t bytecount = 0;

  /* Exec non-blocking on the remote host */
  do {
    channel = libssh2_channel_open_session(session);
    if (channel || libssh2_session_last_error(session, NULL, NULL, 0) !=
                       LIBSSH2_ERROR_EAGAIN)
      break;
    waitsocket(sock, session);
  } while (1);
  if (!channel) {
    fprintf(stderr, "Error\n");
    exit(1);
  }

  // TODO: implement if needed :P
  // if one needs to set more than 42 env. vars - they should increase this
  // valie ^_^ char *varname unsigned int varname_len const char *value unsigned
  // int value_len

  // for (int i =0; i < 42; i++) {
  //     if(envp[i] == NULL) {
  //         break;
  //     }

  //     while((rc = libssh2_channel_setenv_ex(channel, varname, varname_len,
  //     value, value_len) == LIBSSH2_ERROR_EAGAIN) {
  //         waitsocket(sock, session);
  //     }
  //     if(rc) {
  //         fprintf(stderr, "exec error\n");
  //         exit(1);
  //     }
  // }

  while ((rc = libssh2_channel_exec(channel, (const char *)command)) ==
         LIBSSH2_ERROR_EAGAIN) {
    waitsocket(sock, session);
  }
  if (rc) {
    fprintf(stderr, "exec error\n");
    exit(1);
  }
  for (;;) {
    ssize_t nread;
    /* loop until we block */
    do {
      char buffer[0x4000];
      nread = libssh2_channel_read(channel, buffer, sizeof(buffer));
      if (nread > 0) {
        ssize_t i;
        bytecount += nread;
        fprintf(stderr, "We read:\n");
        for (i = 0; i < nread; ++i)
          fputc(buffer[i], stderr);
        fprintf(stderr, "\n");
      } else {
        if (nread != LIBSSH2_ERROR_EAGAIN)
          /* no need to output this for the EAGAIN case */
          fprintf(stderr, "libssh2_channel_read returned %d\n", (int)nread);
      }
    } while (nread > 0);

    /* this is due to blocking that would occur otherwise so we loop on
       this condition */
    if (nread == LIBSSH2_ERROR_EAGAIN) {
      waitsocket(sock, session);
    } else
      break;
  }
  exitcode = 127;
  while ((rc = libssh2_channel_close(channel)) == LIBSSH2_ERROR_EAGAIN)
    waitsocket(sock, session);

  if (rc == 0) {
    exitcode = libssh2_channel_get_exit_status(channel);
    libssh2_channel_get_exit_signal(channel, &exitsignal, NULL, NULL, NULL,
                                    NULL, NULL);
  }

  if (exitsignal)
    fprintf(stderr, "\nGot signal: %s\n", exitsignal);
  else
    fprintf(stderr, "\nEXIT: %d bytecount: %d\n", exitcode, (int)bytecount);

  libssh2_channel_free(channel);
  channel = NULL;

  return exitcode;
}

extern void disconnect_remote(void *c) {
  RTL_REMOTE_CONNECTION *connection = (RTL_REMOTE_CONNECTION *)c;
  LIBSSH2_SESSION *session = connection->session;
  libssh2_socket_t sock = connection->socket;

  if (session) {
    // TODO: we can pass/write arbitrary strings? that's neat'o!
    libssh2_session_disconnect(session, "Normal Shutdown.");
    libssh2_session_free(session);
  }

  if (sock != LIBSSH2_INVALID_SOCKET) {
    shutdown(sock, 2);
#ifdef WIN32
    closesocket(sock);
#else
    close(sock);
#endif
  }

  libssh2_exit();
}