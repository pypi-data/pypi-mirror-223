FROM alpine:latest as compiler

ENV PATH "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/ziglang/"

RUN mkdir -p /opt/rtl /src

WORKDIR /

RUN wget https://ziglang.org/builds/zig-linux-x86_64-0.10.0-dev.3840+2b92c5a23.tar.xz && \
    tar -xvJf /zig-linux-x86_64-0.10.0-dev.3840+2b92c5a23.tar.xz && \
    mv /zig-linux-x86_64-0.10.0-dev.3840+2b92c5a23 /ziglang/ && rm -f /zig-linux-x86_64-0.10.0-dev.3840+2b92c5a23.tar.xz;

RUN apk add --no-cache alpine-sdk clang python3 py3-pip llvm11-dev llvm11 linux-headers && \
    pip3 install -U pip && \
    ln -s /usr/bin/llvm11-config /usr/bin/llvm-config ; 

COPY . /opt/rtl/

RUN cd /opt/rtl && \
    LLVM_CONFIG=/usr/bin/llvm11-config pip3 install . ; \
    rtl || echo '';

WORKDIR /src

ENTRYPOINT ["/usr/bin/rtl"]
