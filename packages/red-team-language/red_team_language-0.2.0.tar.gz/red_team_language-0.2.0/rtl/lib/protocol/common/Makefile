CFLAGS=-O2 -D_FORTIFY_SOURCE=2 -fpie -pie -fstack-protector -flto -Wl,-z,now -Wl,-z,relro -Wformat -Wformat-security -Werror=format-security
RTL_TARGET ?= x86_64-linux-musl

all: common
	@echo

common: rtl_common.c
	@clang -S -emit-llvm -c ${INCLUDES} -no-integrated-as rtl_common.c -Wa,-aln=rtl_common.ll
	@# clang ${CFLAGS} -std=c11 -c -fPIC -Wall rtl_common.c -o rtl_common.o
	@zig cc ${CFLAGS} ${INCLUDES} -target ${RTL_TARGET} -c -fPIC -Wall rtl_common.c -o rtl_common.o

main: common
	@# clang ${CFLAGS} -std=c11 -fPIC -Wall rtl_common.o main.c -o main
	@zig cc ${CFLAGS} ${INCLUDES} -target ${RTL_TARGET} -fPIC -Wall rtl_common.o main.c -o main -Wl,-s

clean:
	@rm -f rtl_common.ll rtl_common.o main &> /dev/null || echo
