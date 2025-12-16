import sys
import os

BUILTINS = {"exit", "echo", "type"}

def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        line = sys.stdin.readline()
        if not line:
            continue

        parts = line.strip().split()
        if not parts:
            continue
        cmd = parts[0]
        args = parts[1:]

        if cmd == 'exit':
            return
        
        if cmd == 'echo':
            print(" ".join(args))
            continue

        if cmd == "type":
            if not args:
                continue
            target = args[0]

            # 1.builtin check
            if target in BUILTINS:
                print(f"{target} is a shell builtin")
                continue

            # 2. PATH search
            for directory in os.environ.get("PATH", "").split(os.pathsep):
                full_path = os.path.join(directory, target)
                if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                    print(f"{target} is {full_path}")
                    break
                    
            else:
                print(f"{target}: not found")
            continue


        print(f"{cmd}: command not found")




if __name__ == "__main__":
    main()


