import sys
import os
import subprocess

BUILTINS = {"exit", "echo", "type", "pwd", "cd"}

def find_executable(cmd):
    for directory in os.environ.get("PATH", "").split(os.pathsep):
        full_path = os.path.join(directory, cmd)
        if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
            return full_path
    return None

def parse_command(line):
    args = []
    current = ""
    in_single_quote = False
    in_double_quote = False

    for ch in line:
        # Toggle single quotes (only if not inside double quotes)
        if ch == "'" and not in_double_quote:
            in_single_quote = not in_single_quote

        # Toggle double quotes (only if not inside single quotes)
        elif ch == '"' and not in_single_quote:
            in_double_quote = not in_double_quote

        # Split on space only if not inside any quotes
        elif ch == " " and not in_single_quote and not in_double_quote:
            if current:
                args.append(current)
                current = ""

        # All other characters are literal
        else:
            current += ch

    # Append last argument if present
    if current:
        args.append(current)

    return args



def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        line = sys.stdin.readline()
        if not line:
            continue

        parts = parse_command(line.rstrip("\n"))
        if not parts:
            continue

        cmd = parts[0]
        args = parts[1:]

        if cmd == "exit":
            return

        if cmd == "echo":
            print(" ".join(args))
            continue

        if cmd == "pwd":
            print(os.getcwd())
            continue
        
        if cmd == "cd":
            if not args:
                continue

            path = args[0]

            if path == '~':
                path = os.getenv("HOME")

            try:
                os.chdir(path)
            except FileNotFoundError:
                print(f"cd: {path}: No such file or directory")
            except NotADirectoryError:
                print(f"cd: {path}: Not a directory")
            except PermissionError:
                print(f"cd: {path}: Permission denied")
            continue



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

        exe_path = find_executable(cmd)
        if exe_path:
            subprocess.run([cmd] + args, executable=exe_path)
        else:
            print(f"{cmd}: command not found")

if __name__ == "__main__":
    main()
