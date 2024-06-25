import sys
import zlib
import hashlib
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
            blob_object = sys.argv[3]
            blob_path = f".git/objects/{blob_object[:2]}/{blob_object[2:]}"
            if not os.path.exists(blob_path):
                print(f"The blob object {blob_object} does not exist.")
                return
            obj = sys.argv[3]
            with open(f".git/objects/{obj[:2]}/{obj[2:]}", "rb") as f:
                data = zlib.decompress(f.read())
                header, content = data.split(b"\0", maxsplit=1)
                print(content.decode(), end="")
        elif sys.argv[2] != "-p":
            print("Unknown flag")
        else:
            print("Please provide an object to print.")
    elif command == "hash-object":
        if len(sys.argv) > 3 and sys.argv[2] == "-w":
            file_path = sys.argv[3]
            if not os.path.exists(file_path):
                print(f"The path {file_path} does not exist.")
                return
            with open(sys.argv[3], "rb") as f:
                data = f.read()
                header = f"blob {len(data)}\0".encode()
                store = header + data
                sha1 = hashlib.sha1(store).hexdigest()
                os.makedirs(f".git/objects/{sha1[:2]}", exist_ok=True)
                with open(f".git/objects/{sha1[:2]}/{sha1[2:]}", "wb") as f_out:
                    f_out.write(zlib.compress(store))
                print(sha1)
        elif sys.argv[2] != "-w":
            print("Unknown flag")
        else:
            print("Please provide a file to hash.")
    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
