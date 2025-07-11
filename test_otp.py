import hashlib
import os
from io import DEFAULT_BUFFER_SIZE

import pytest

from otp import decrypt, encrypt

TMP_DIR = "test_files"


@pytest.fixture(scope="module", autouse=True)
def setup_teardown():
    os.makedirs(TMP_DIR, exist_ok=True)
    yield
    for f in os.listdir(TMP_DIR):
        os.remove(os.path.join(TMP_DIR, f))


def write_file(path: str, data: bytes):
    with open(path, "wb") as f:
        f.write(data)


def file_hash(path: str) -> bytes:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(DEFAULT_BUFFER_SIZE):
            h.update(chunk)
    return h.digest()


def encrypt_decrypt_and_compare(input_file, key_file, enc_file, dec_file):
    with open(input_file, "rb") as f_plain, open(key_file, "wb") as f_key, open(
        enc_file, "wb"
    ) as f_enc:
        encrypt(f_plain, f_key, f_enc)

    with open(enc_file, "rb") as f_enc, open(key_file, "rb") as f_key, open(
        dec_file, "wb"
    ) as f_dec:
        decrypt(f_enc, f_key, f_dec)

    return file_hash(input_file) == file_hash(dec_file)


def test_encrypt_decrypt_text():
    input_path = os.path.join(TMP_DIR, "original.txt")
    write_file(input_path, b"Top secret! Top secret!\n")

    assert encrypt_decrypt_and_compare(
        input_file=input_path,
        key_file=os.path.join(TMP_DIR, "key.bin"),
        enc_file=os.path.join(TMP_DIR, "enc.bin"),
        dec_file=os.path.join(TMP_DIR, "dec.txt"),
    )


def test_empty_file():
    input_path = os.path.join(TMP_DIR, "empty.txt")
    write_file(input_path, b"")

    assert encrypt_decrypt_and_compare(
        input_file=input_path,
        key_file=os.path.join(TMP_DIR, "empty_key.bin"),
        enc_file=os.path.join(TMP_DIR, "empty.enc"),
        dec_file=os.path.join(TMP_DIR, "empty.dec"),
    )


def test_large_file():
    input_path = os.path.join(TMP_DIR, "large.txt")
    write_file(input_path, os.urandom(5 * 1024 * 1024))  # 5 MB

    assert encrypt_decrypt_and_compare(
        input_file=input_path,
        key_file=os.path.join(TMP_DIR, "large_key.bin"),
        enc_file=os.path.join(TMP_DIR, "large.enc"),
        dec_file=os.path.join(TMP_DIR, "large.dec"),
    )
