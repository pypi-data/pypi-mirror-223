CFLAGS=-O2 -D_FORTIFY_SOURCE=2 -fpie -pie -fstack-protector -flto -Wl,-z,now -Wl,-z,relro -Wformat -Wformat-security -Werror=format-security
RTL_TARGET ?= x86_64-linux-musl

all: xor
	@echo

xor:
	@clang -S -emit-llvm -c -no-integrated-as xor.c -Wa,-aln=xor.ll
	@# clang ${CFLAGS} -std=c11 -c -fPIC -Wall xor.c -o xor.o
	@zig cc ${CFLAGS} -target ${RTL_TARGET} -c -fPIC -Wall xor.c -o xor.o


main: xor
	@# clang ${CFLAGS} -std=c11 -fPIC -Wall xor.o main.c -o main
	@zig cc ${CFLAGS} -target ${RTL_TARGET} -fPIC -Wall xor.o main.c -o main -Wl,-s

clean:
	@rm xor.ll xor.o main &> /dev/null || echo
