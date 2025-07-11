import os
import sys
from io import DEFAULT_BUFFER_SIZE, BufferedReader, BufferedWriter
from pathlib import Path

USAGE = """
python3 otp.py -[e|d] <input_file> <key_file> <output_file>

-d: decrypt
-e: encrypt
"""


def decrypt(
    enc_file: BufferedReader, key_in: BufferedReader, plain_file: BufferedWriter
) -> None:
    while enc_chunk := enc_file.read(DEFAULT_BUFFER_SIZE):
        key_c = key_in.read(len(enc_chunk))
        if len(key_c) != len(enc_chunk):
            raise ValueError("Key file is shorter than encrypted file.")

        plain = bytes(a ^ b for a, b in zip(key_c, enc_chunk))
        plain_file.write(plain)


def encrypt(
    plain_file: BufferedReader, key_out: BufferedWriter, enc_file: BufferedWriter
) -> None:
    while chunk := plain_file.read(DEFAULT_BUFFER_SIZE):
        key = os.urandom(len(chunk))
        enc_c = bytes(a ^ b for a, b in zip(chunk, key))

        enc_file.write(enc_c)
        key_out.write(key)


def main() -> None:
    argc = len(sys.argv)
    if argc != 5:
        print(USAGE)
        sys.exit(1)

    mode = sys.argv[1]
    key_path = Path(sys.argv[3])
    output_path = Path(sys.argv[4])
    input_path = Path(sys.argv[2])

    # fmt: off
    if mode == "-e":

        with open(input_path, "rb") as input_file, \
            open(key_path, "wb") as key_file, \
            open(output_path, "wb") as output_file:

            encrypt(input_file, key_file, output_file)

    elif mode == "-d":

        with open(input_path, "rb") as input_file, \
            open(key_path, "rb") as key_file, \
            open(output_path, "wb") as output_file:

            decrypt(input_file, key_file, output_file)
    # fmt: on

    else:
        print(f"Invalid mode: {mode}")
        print(USAGE)
        sys.exit(1)


if __name__ == "__main__":
    main()
