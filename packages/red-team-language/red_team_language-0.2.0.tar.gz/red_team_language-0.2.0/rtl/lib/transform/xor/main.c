#include <stdio.h>
#include <string.h>
#include <stdlib.h>

extern unsigned char * transform_xor(unsigned char *, unsigned char *, int, int);
extern unsigned char * transform_xor_machineid();
extern unsigned char * transform_xor_bootid();
extern unsigned char * transform_xor_uid();

int main(int argc, char *argv[]) {
    unsigned char key[] = "thisisthekey";
    unsigned char pt[] = "thisistheplaintext";

    int klen = strlen((char*)key);
    int ptlen = strlen((char*)pt);

    printf("PT :\n\t%s\n", pt);
    unsigned char* ct = transform_xor(key, pt, klen, ptlen);

    printf("CT: \n\t");
    for(int i = 0; i < ptlen; i ++) {
        printf("0x%0.2x ", pt[i]);
        if ((i+1) % 16 == 0) {
            printf("\n\t");
        }
    }
    printf("\n");

    ct = transform_xor(key, ct, klen, ptlen);

    printf("PT :\n\t%s\n", ct);

    unsigned char* machineid = transform_xor_machineid();

    printf("\n\nmachineID: %s\n", machineid);

    printf("\n\nbootid: %s\n", transform_xor_bootid());

    unsigned char* bytes = transform_xor_uid();

    printf("%x %x %x %x\n", (unsigned char)bytes[0],
                            (unsigned char)bytes[1],
                            (unsigned char)bytes[2],
                            (unsigned char)bytes[3]);

    return EXIT_SUCCESS;
}