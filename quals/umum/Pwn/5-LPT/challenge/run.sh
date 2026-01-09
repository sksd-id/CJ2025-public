#!/bin/bash

QEMU_ENV="REMOTE=no"
if [ $# -eq 1 ]; then
    QEMU_ENV="REMOTE=yes"
fi

timeout --foreground 90 qemu-system-x86_64 \
    -cpu qemu64,+la57 \
    -m 256M \
    -smp 1 \
    -kernel bzImage \
    -initrd initramfs.cpio.gz \
    -nographic \
    -monitor /dev/null \
    -no-reboot \
    -drive file=flag,if=virtio,format=raw,readonly=on \
    -append "console=ttyS0 kaslr rdinit=/sbin/init pti=on oops=panic panic=1 quiet $QEMU_ENV"

