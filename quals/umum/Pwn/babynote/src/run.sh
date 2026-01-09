#!/bin/sh
socat tcp-l:13373,reuseaddr,fork exec:"/home/ctf/babynote"