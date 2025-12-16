import sys
BUILTINS = {"echo", "exit", "type"}
def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush() # for exiting the buffer

        line = sys.stdin.readline() #input from user saved in line
        if not line:
            continue

        command = line.strip()
        if not command:
            continue
        parts = command.split()
        cmd = parts[0]
        args = parts[1:]

        # exit builtin
        if cmd == "exit":
            return # terminate the shell

        # echo button
        if cmd == "type":
            if len(args) == 0:
                continue # no arguement given ignore
            target = args[0]
            if target in BUILTINS:
                print(f"{target}: is a shell builtin")
            else:
                print(f"{target}: not found")
            continue

        

        if command: # else print this below
            print(f"{command}: command not found")

if __name__ == "__main__":
    main()

