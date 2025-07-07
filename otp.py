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
    if argc <= 2:
        print(USAGE)
        sys.exit(1)


if __name__ == "__main__":
    main()
