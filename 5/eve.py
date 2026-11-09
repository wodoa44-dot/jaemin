import argparse
import base64
import json
import math
import sys
from pathlib import Path


def recover_private_key(n, e):
    if type(n) is not int or not 400**2 <= n <= 500**2:
        raise ValueError('Expected the assignment RSA modulus (400 <= p,q <= 500).')
    for p in range(2, math.isqrt(n) + 1):
        if n % p == 0:
            q = n // p
            if p == q:
                raise ValueError('Expected distinct RSA primes.')
            phi = (p - 1) * (q - 1)
            return p, q, pow(e, -1, phi)
    raise ValueError('Cannot factor RSA modulus.')


class Eve:
    def __init__(self):
        self.n = self.d = self.key = None
        self.count = 0
        self.total = 0

    def observe(self, message):
        opcode, kind = message.get('opcode'), message.get('type')
        if opcode == 0:
            self.n = self.d = self.key = None
            self.count = 0
        elif opcode == 1 and kind == 'RSA':
            self.key = None
            self.count = 0
            n, e = message['parameter']['n'], message['public']
            if isinstance(e, str):
                e = int.from_bytes(base64.b64decode(e, validate=True), 'big')
            p, q, d = recover_private_key(n, e)
            self.n, self.d = n, d
            print(f'[Eve] n={n}, e={e}; factored p={p}, q={q}; recovered d={d}', flush=True)
        elif opcode == 2 and kind == 'RSA':
            if self.d is None:
                raise ValueError('Missing preceding RSA public-key message.')
            encrypted = message['encrypted_key']
            if not isinstance(encrypted, list) or len(encrypted) != 32:
                raise ValueError('Expected 32 RSA-encrypted key bytes.')
            if any(type(c) is not int or not 0 <= c < self.n for c in encrypted):
                raise ValueError('Invalid RSA ciphertext integer.')
            self.key = bytes(pow(c, self.d, self.n) for c in encrypted)
            print(f'[Eve] Recovered AES-256 key: {self.key.hex()}', flush=True)
        elif opcode == 2 and kind == 'AES':
            if self.key is None:
                raise ValueError('Missing preceding RSA-encrypted AES key.')
            from Crypto.Cipher import AES
            from Crypto.Util.Padding import unpad
            ciphertext = base64.b64decode(message['encryption'], validate=True)
            plaintext = unpad(AES.new(self.key, AES.MODE_ECB).decrypt(ciphertext), 16).decode('utf-8')
            self.count += 1
            self.total += 1
            direction = {1: 'Responder -> Initiator', 2: 'Initiator -> Responder'}.get(self.count, 'AES message')
            print(f'[Eve] {direction}: {plaintext}', flush=True)
            return plaintext


def messages(lines):
    for line in lines:
        # Only JSON protocol objects are consumed; plaintext log lines are ignored.
        stripped = line.strip()
        if stripped.startswith('{'):
            text = stripped
        elif 'Sent: ' in line or 'Received: ' in line:
            text = line[line.find('{'):] if '{' in line else ''
        else:
            continue
        if text:
            item = json.loads(text)
            if not isinstance(item, dict):
                raise ValueError('Expected a JSON object.')
            yield item


def main():
    parser = argparse.ArgumentParser(description='Additional Task I: passive RSA recovery from one endpoint transcript.')
    parser.add_argument('--log', type=Path, help='Alice OR Bob transcript; omit to read standard input live.')
    args = parser.parse_args()
    eve = Eve()
    try:
        if args.log:
            data = args.log.read_bytes()
            text = data.decode('utf-16' if data.startswith((b'\xff\xfe', b'\xfe\xff')) else 'utf-8-sig')
            source = text.splitlines()
        else:
            source = sys.stdin
        for message in messages(source):
            eve.observe(message)
        if not eve.total:
            raise ValueError('No AES message recovered. Supply a complete Protocol II transcript.')
    except (OSError, ValueError, KeyError, TypeError, OverflowError) as exc:
        print(f'[Eve] ERROR: {exc}', file=sys.stderr)
        return 1
    except ModuleNotFoundError:
        print('[Eve] Install dependency: python -m pip install pycryptodome', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
