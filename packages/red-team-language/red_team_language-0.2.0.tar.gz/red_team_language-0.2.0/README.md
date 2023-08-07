# Install!

```bash
pip3 install .
```

# Usage

```bash
usage: rtl [-h] --src SRC [--dst DST] [--ir] [--asm] [--obj] [--build]

The Red-Team-Language compiler enables one to write scripts and deploy them as static executables - for the lolz of course!

options:
  -h, --help  show this help message and exit
  --src SRC   The source *.rtl script to compile to LLVM-IR
  --dst DST   The where to write the output (default is stdout)
  --ir        Emit LLVM-IR
  --asm       Emit assembly for this machine
  --obj       Emit an object file for this machine
  --build     Attempt to build a binary from the provided --src
```

NOTE: _The `--build` flag requires the ziglang binary 'zig' be on path if not using docker; this is the way._

```bash
rtl --src rtl/examples/shell/shell_executable.rtl --asm > a.s
clang -o executable.elf -fPIC rtl/lib/protocol/shell/shell.o rtl/lib/transform/xor/xor.o a.s -ggdb
```

# Docker

Pick a file from `./rtl/examples/shell` and execute the following - or use the one provided and copy+pasta! _(i.e. executable_script_inline_obfuscated.rtl)_

```bash
DOCKER_BUILDKIT=1 docker build -f Dockerfile -t rtl:latest .
docker run --rm -it --volume "`pwd`/rtl/examples/shell/:/src" --volume "`pwd`/tmp:/tmp" rtl --src /src/executable_script_inline_obfuscated.rtl --build
ls -alh ./tmp
file ./tmp/*
```
