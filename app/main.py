import sys
import os
import subprocess

BUILTINS = {"exit", "echo", "type"}

def find_executable(cmd):
    for directory in os.environ.get("PATH", "").split(os.pathsep):
        full_path = os.path.join(directory, cmd)
        if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
            return full_path
    return None

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

        # exit builtin
        if cmd == "exit":
            return

        # echo builtin
        if cmd == "echo":
            print(" ".join(args))
            continue

        # type builtin
        if cmd == "type":
            if not args:
                continue

            target = args[0]

            if target in BUILTINS:
                print(f"{target} is a shell builtin")
                continue

            exe_path = find_executable(target)
            if exe_path:
                print(f"{target} is {exe_path}")
            else:
                print(f"{target}: not found")
            continue

        # external command execution
        exe_path = find_executable(cmd)
        if exe_path:
            subprocess.run([exe_path] + args)
        else:
            print(f"{cmd}: command not found")

if __name__ == "__main__":
    main()
