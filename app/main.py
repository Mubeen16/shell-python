import sys

def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush() # for exiting the buffer

        line = sys.stdin.readline() #input from user saved in line
        if not line:
            continue

        command = line.strip()
        if command == "exit":
            break # terminate the shell

        if command: # else print this below
            print(f"{command}: command not found")

if __name__ == "__main__":
    main()

