import base64
import math
import secrets


def is_prime(n):
    if type(n) is not int or n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    return all(n % d for d in range(3, math.isqrt(n) + 1, 2))


def extended_gcd(a, b):
    old_r, r, old_s, s, old_t, t = a, b, 1, 0, 0, 1
    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    return old_r, old_s, old_t


def inverse(a, modulus):
    gcd, x, _ = extended_gcd(a, modulus)
    if gcd != 1:
        raise ValueError('inverse does not exist')
    return x % modulus


def prime_factors(n):
    factors = set()
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.add(d)
            n //= d
        d += 1
    if n > 1:
        factors.add(n)
    return factors


def is_generator(g, p):
    return (is_prime(p) and type(g) is int and 1 < g < p
            and all(pow(g, (p - 1) // r, p) != 1 for r in prime_factors(p - 1)))


def random_prime():
    return secrets.choice([n for n in range(400, 501) if is_prime(n)])


def rsa_keypair():
    p, q = random_prime(), random_prime()
    while q == p:
        q = random_prime()
    phi = (p - 1) * (q - 1)
    e = 65537
    while math.gcd(e, phi) != 1:
        e = secrets.randbelow(phi - 2) + 2
    return p, q, e, inverse(e, phi)


def verify_rsa(p, q, e, d):
    return (is_prime(p) and is_prime(q) and p != q
            and 400 <= p <= 500 and 400 <= q <= 500
            and type(e) is int and type(d) is int and e > 1 and d > 0
            and math.gcd(e, (p - 1) * (q - 1)) == 1
            and e * d % ((p - 1) * (q - 1)) == 1)


def dh_parameters():
    p = random_prime()
    g = next(g for g in range(2, p) if is_generator(g, p))
    return p, g


def dh_private(p):
    return secrets.randbelow(p - 2) + 1


def dh_aes_key(shared):
    return shared.to_bytes(2, byteorder='big') * 16


def public_integer(value):
    if type(value) is int:
        return value
    if isinstance(value, str):
        return int.from_bytes(base64.b64decode(value, validate=True), 'big')
    raise ValueError('invalid public key')


def encrypt(key, message):
    from Crypto.Cipher import AES
    data = message.encode('utf-8')
    padding = 16 - len(data) % 16
    return base64.b64encode(AES.new(key, AES.MODE_ECB).encrypt(
        data + bytes([padding]) * padding)).decode('ascii')


def decrypt(key, encoded):
    from Crypto.Cipher import AES
    data = base64.b64decode(encoded, validate=True)
    if not data or len(data) % 16:
        raise ValueError('invalid AES ciphertext length')
    plain = AES.new(key, AES.MODE_ECB).decrypt(data)
    padding = plain[-1]
    if not 1 <= padding <= 16 or plain[-padding:] != bytes([padding]) * padding:
        raise ValueError('invalid AES padding')
    return plain[:-padding].decode('utf-8')
