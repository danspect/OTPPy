import sys
from sys import byteorder as SYS_BYTEORDER
from pathlib import Path
import secrets
from io import BufferedReader, BufferedWriter

USAGE = """
python3 otp.py -[d|e] [key] [encrypted] [plain]

-d: decrypt
-e: encrypt
"""


def decrypt(
    enc_file: BufferedReader, key_in: BufferedReader, plain_file: BufferedWriter
) -> None:
    while enc_chunk := enc_file.read(1):
        key_c = key_in.read(1)
        if not key_c:
            raise ValueError("Key file is shorter than encrypted file.")

        plain = key_c[0] ^ enc_chunk[0]
        plain_file.write(plain.to_bytes(1, SYS_BYTEORDER))


def encrypt(
    plain_file: BufferedReader, key_out: BufferedWriter, enc_file: BufferedWriter
) -> None:
    while chunk := plain_file.read(1):
        key = secrets.randbits(8)
        enc_c = key ^ chunk[0]

        enc_file.write(enc_c.to_bytes(1, SYS_BYTEORDER))
        key_out.write(key.to_bytes(1, SYS_BYTEORDER))


def main() -> None:
    argc = len(sys.argv)
    if argc != 5:
        print(USAGE)
        sys.exit(1)

    mode = sys.argv[1]
    key_path = Path(sys.argv[2])
    encrypted_path = Path(sys.argv[3])
    plain_path = Path(sys.argv[4])

    if mode == "-e":
        with open(plain_path, "rb") as plain_file, \
            open(key_path, "wb") as key_file, \
            open(encrypted_path, "wb") as enc_file:

            encrypt(plain_file, key_file, enc_file)
    if mode == "-d":
        with open(plain_path, "wb") as plain_file, \
            open(key_path, "rb") as key_file, \
            open(encrypted_path, "rb") as enc_file:

            decrypt(enc_file, key_file, plain_file)


if __name__ == "__main__":
    main()
