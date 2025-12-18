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
    escape_next = False
    i = 0

    while i < len(line):
        ch = line[i]

        if escape_next:
            current += ch
            escape_next = False
            i += 1
            continue

        if ch == "\\" and not in_single_quote and not in_double_quote:
            escape_next = True
            i += 1
            continue

        if ch == "\\" and in_double_quote:
            if i + 1 < len(line) and line[i + 1] in ['"', '\\']:
                current += line[i + 1]
                i += 2
            else:
                current += "\\"
                i += 1
            continue

        if ch == "'" and not in_double_quote:
            in_single_quote = not in_single_quote
            i += 1
            continue

        if ch == '"' and not in_single_quote:
            in_double_quote = not in_double_quote
            i += 1
            continue

        if ch == " " and not in_single_quote and not in_double_quote:
            if current:
                args.append(current)
                current = ""
            i += 1
            continue

        current += ch
        i += 1

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

        # ----------------------------
        # Handle stdout redirection (>, 1>)
        # ----------------------------
        redirect_file = None
        redirect_idx = None

        for i, token in enumerate(parts):
            if token == ">" or token == "1>":
                redirect_idx = i
                redirect_file = parts[i + 1]
                break

        if redirect_idx is not None:
            parts = parts[:redirect_idx]


        cmd = parts[0]
        args = parts[1:]

        # ----------------------------
        # Builtins
        # ----------------------------
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
            if path == "~":
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

        # ----------------------------
        # External commands
        # ----------------------------
        exe_path = find_executable(cmd)
        if not exe_path:
            print(f"{cmd}: command not found")
            continue

        if redirect_file:
            saved_stdout = os.dup(1)
            fd = os.open(
                redirect_file,
                os.O_WRONLY | os.O_CREAT | os.O_TRUNC,
                0o644
            )
            os.dup2(fd, 1)
            os.close(fd)

            try:
                subprocess.run([cmd] + args, executable=exe_path)
            finally:
                os.dup2(saved_stdout, 1)
                os.close(saved_stdout)
        else:
            subprocess.run([cmd] + args, executable=exe_path)


if __name__ == "__main__":
    main()
