CFLAGS=-O2 -D_FORTIFY_SOURCE=2 -fpie -pie -fstack-protector -flto -Wl,-z,now -Wl,-z,relro -Wformat -Wformat-security -Werror=format-security
RTL_TARGET ?= x86_64-linux-musl
INCLUDES=-I../common/

all: shell
	@echo

rtl_common.o:
	@make -C ../common/
	@cp ../common/rtl_common.o ./

shell: rtl_common.o
	@clang -S -emit-llvm -c ${INCLUDES} -no-integrated-as shell.c -Wa,-aln=shell.ll
	@# clang ${CFLAGS} -std=c11 -c -fPIC -Wall shell.c -o shell.o
	@zig cc ${CFLAGS} -target ${RTL_TARGET} -c -fPIC -Wall shell.c -o shell.o


main: shell
	@# clang ${INCLUDES} ${CFLAGS} -std=c11 -fPIC -Wall shell.o main.c -o main
	@zig cc ${INCLUDES} ${CFLAGS} -target ${RTL_TARGET} -fPIC -Wall shell.o rtl_common.o main.c -o main -Wl,-s

clean:
	@rm -f shell.ll shell.o rtl_common.o main &> /dev/null || echo
	@make -C ../common/ clean; 
