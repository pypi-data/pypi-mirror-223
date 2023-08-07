#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <inttypes.h>


unsigned char * transform_xor(unsigned char *key, unsigned char *plaintext, int keyLen, int ptLen)
{
    int idx;
    for (idx = 0; idx < ptLen; idx++)
    {
        plaintext[idx] = plaintext[idx] ^ key[idx % keyLen];
    }

    return plaintext;
}


unsigned char * get_file_contents(char* filepath, int max_read)
{
    unsigned char *machineid = (unsigned char *) calloc(max_read, 1);

    if (machineid == NULL) {
        return (unsigned char *) "                                ";
    }

    FILE *fd = fopen(filepath, "r");

    if (fd == NULL)
    {
        return machineid;
    }

    fread(machineid, 1, max_read - 1, fd);

    fclose(fd);

    return machineid;
}

unsigned char * transform_xor_machineid() {
    return get_file_contents("/var/lib/dbus/machine-id", 33);
}

unsigned char * transform_xor_bootid() {
    return get_file_contents("/proc/sys/kernel/random/boot_id", 37);
}

unsigned char * transform_xor_uid() {
    unsigned char * bytes = (unsigned char *)calloc(4, 1);

    unsigned long n = getuid();

    bytes[0] = (n >> 24) & 0xFF;
    bytes[1] = (n >> 16) & 0xFF;
    bytes[2] = (n >> 8) & 0xFF;
    bytes[3] = n & 0xFF;

    return bytes;
}