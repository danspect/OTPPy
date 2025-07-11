# OTPPy

is a lightweight, high-security encryption tool that implements the
[One-Time Pad](https://en.wikipedia.org/wiki/One-time_pad) algorithm — the only proven method of encryption that is theoretically unbreakable when used properly.

This tool enables the encryption and decryption of binary or text files using a key of equal or greater length, with perfect secrecy.
> [!WARNING]
> OTP requires that keys are random, used only once, and kept secret. Failing to meet these criteria compromises security.
>

## Features

- Encrypt and decrypt files using the OTP algorithm

- Simple command-line interface

- Supports any file format (binary or text)

- No dependencies outside the Python standard library

## Usage

Basic command format:

```bash
python3 otp.py -[e|d] <input_file> <key_file> <output_file>
```

### Parameters

| Argument        | Description                                      |
| --------------- | ------------------------------------------------ |
| `-e`            | Encrypt mode                                     |
| `-d`            | Decrypt mode                                     |
| `<key_file>`    | File containing the one-time pad (key) in binary |
| `<input_file>`  | Input file to be encrypted or decrypted          |
| `<output_file>` | Output file (encrypted or decrypted result)      |

## Examples

Encrypting a file:

```bash
python3 otp.py -e input.txt key.bin output.enc 
```

- Encrypts input.txt using key.bin
- Saves the result to output.enc

Decrypting a file

```bash
python3 otp.py -d input.enc key.bin output.txt
```

- Decrypts input.enc using key.bin
- Restores original content into output.txt

## Security Best Practices

To ensure the theoretical security of OTP:

- Generate keys using cryptographically secure methods (e.g., `os.urandom`)

- Never reuse a key (use once and discard)

- Distribute the key through a secure channel

- Do not store the key alongside the encrypted file

- Ensure the key is as long as the file to be encrypted

## License

This project is open-source and released under the MIT License.
