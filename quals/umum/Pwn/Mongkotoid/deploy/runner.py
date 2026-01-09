import sys
import uuid
import subprocess
import signal

def timeout_handler(signum, frame):
    print("Timeout reached. Exiting.", flush=True)
    exit(-1)

# Set the signal for timeout
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(30)  # Set timeout to 60 seconds

filename = f"/tmp/{str(uuid.uuid4())}"

print("Please send your own payload! (receive until '<EOF>'), Max: 100000bytes", flush=True)

byt = 0
with open(filename, "w") as f:
    while byt < 100000:
        line = sys.stdin.readline()

        if "<EOF>" in line:
            break

        if len(line) + byt > 100000:
            print(f"{byt + len(line)} > 100000, Assert", flush=True)
            exit(-1)
        else:
            f.write(line)

signal.alarm(0)

subprocess.run(["/home/pwn/js", f"{filename}"])