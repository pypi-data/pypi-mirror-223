CFLAGS=-O2 -D_FORTIFY_SOURCE=2 -fpie -pie -fstack-protector -flto -Wl,-z,now -Wl,-z,relro -Wformat -Wformat-security -Werror=format-security
RTL_TARGET ?= x86_64-linux-musl
INCLUDES=-I./libssh2/include/ -I../common/
LIBRARY_PATHS=-L./libssh2/build/src -L./mbedtls/build/library

all: ssh
	@echo

rtl_common.o:
	@make -C ../common/
	@cp ../common/rtl_common.o ./

libssh2/build/src/libssh2.a:
	@mkdir libssh2/build ; \
		cd libssh2/build ; \
		cmake -DBUILD_SHARED_LIBS=OFF -DENABLE_ZLIB_COMPRESSION=OFF -DENABLE_CRYPT_NONE=ON -DBUILD_EXAMPLES=OFF -DBUILD_TESTING=OFF -DENABLE_MAC_NONE=ON CLEAR_MEMORY=ON -DCRYPTO_BACKEND=mbedTLS ../ ; \
		cmake --build . --config Release

mbedtls/build/library/libmbedcrypto.a: 
	@mkdir mbedtls/build ; \
		cd mbedtls/build ; \
		# -DCMAKE_BUILD_TYPE=Release ... doesn't work for some reason... ld.lld: error: undefined symbol: __printf_chk \
		cmake -DDISABLE_PACKAGE_CONFIG_AND_INSTALL=On -DENABLE_PROGRAMS=Off -DENABLE_TESTING=Off -DUSE_SHARED_MBEDTLS_LIBRARY=Off ../ ; \
		cmake --build . --config Release

ssh: rtl_common.o mbedtls/build/library/libmbedcrypto.a libssh2/build/src/libssh2.a ssh.c
	@clang -S -emit-llvm -c ${INCLUDES} -no-integrated-as ssh.c -Wa,-aln=ssh.ll
	@zig cc ${CFLAGS} ${INCLUDES} -target ${RTL_TARGET} -c -fPIC -Wall ssh.c -o ssh.o

main: ssh
	@# clang ${CFLAGS} -std=c11 -fPIC -Wall ssh.o main.c -o main
	@zig cc ${INCLUDES} ${CFLAGS} -target ${RTL_TARGET} -fPIC -Wall ssh.o rtl_common.o main.c -o main -Wl,-s ${LIBRARY_PATHS} -lssh2 -lmbedtls -lmbedcrypto -lmbedx509

clean:
	@# rm -rf libssh2/build
	@# rm -rf mbedtls/build
	@rm -f ssh.ll ssh.o rtl_common.o main &> /dev/null || echo
	@make -C ../common/ clean
