#ifndef _RTL_PROTOCOL_COMMON_H
#define _RTL_PROTOCOL_COMMON_H

#define DEBUG 1

extern unsigned char **rtl_parse_protocol_argument_buffer(unsigned char *buf);
extern int rtl_get_argument_index(unsigned char **argv, unsigned char *key);

#endif