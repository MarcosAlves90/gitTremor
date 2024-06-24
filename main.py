import sys
import zlib
import os


def main():

    command = sys.argv[1]
    if command == "init":
        os.mkdir(".git")
        os.mkdir(".git/objects")
        os.mkdir(".git/refs")
        with open(".git/HEAD", "w") as f:
            f.write("ref: refs/heads/main\n")
        print("Initialized git directory")
    elif command == "cat-file":
        if len(sys.argv) > 3 and sys.argv[2] == "-p":
            obj = sys.argv[3]
            with open(f".git/objects/{obj[:2]}/{obj[2:]}", "rb") as f:
                data = zlib.decompress(f.read())
                header, content = data.split(b"\0", maxsplit=1)
                print(content.decode(), end="")
        else:
            print("Please provide an object to print.")
    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
