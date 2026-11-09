import codecs
import json
import logging
import secrets
from crypto_math import (is_prime, is_generator, rsa_keypair, verify_rsa,
                         dh_parameters, dh_private, dh_aes_key, public_integer,
                         encrypt, decrypt)


class RemoteError(Exception):
    pass


class Channel:
    def __init__(self, sock):
        self.sock = sock
        self.buffer = ''
        self.decoder = codecs.getincrementaldecoder('utf-8')()
        self.json_decoder = json.JSONDecoder()

    def send(self, message):
        data = json.dumps(message, ensure_ascii=True)
        self.sock.sendall(data.encode('ascii'))
        logging.info('Sent: %s', data)

    def receive(self):
        while True:
            self.buffer = self.buffer.lstrip()
            if self.buffer:
                try:
                    value, end = self.json_decoder.raw_decode(self.buffer)
                except json.JSONDecodeError:
                    pass
                else:
                    self.buffer = self.buffer[end:]
                    if not isinstance(value, dict):
                        raise ValueError('expected JSON object')
                    logging.info('Received: %s', json.dumps(value))
                    if value.get('opcode') == 3:
                        raise RemoteError(value.get('error', 'remote error'))
                    return value
            chunk = self.sock.recv(4096)
            if not chunk:
                raise ValueError('connection closed before a complete JSON message')
            self.buffer += self.decoder.decode(chunk)
            if len(self.buffer) > 4 * 1024 * 1024:
                raise ValueError('message too large')


def expect(message, opcode, kind):
    if message.get('opcode') != opcode or message.get('type') != kind:
        raise ValueError('unexpected protocol message')
    return message


def validate_dh(message):
    p, g = message['parameter']['p'], message['parameter']['g']
    if not is_prime(p):
        raise ValueError('incorrect prime number')
    if not 400 <= p <= 500:
        raise ValueError('prime number outside 400..500')
    if not is_generator(g, p):
        raise ValueError('incorrect generator')
    public = public_integer(message['public'])
    if not 1 <= public < p:
        raise ValueError('invalid DH public key')
    return p, g, public


def receive_aes(channel, key):
    message = expect(channel.receive(), 2, 'AES')
    plaintext = decrypt(key, message['encryption'])
    logging.info('Decrypted: %s', plaintext)
    return plaintext


def send_aes(channel, key, message):
    channel.send({'opcode': 2, 'type': 'AES', 'encryption': encrypt(key, message)})


def initiate(channel, kind, message):
    channel.send({'opcode': 0, 'type': kind})
    reply = channel.receive()
    if kind == 'RSAKey':
        expect(reply, 0, kind)
        p, q = reply['parameter']['p'], reply['parameter']['q']
        e, d = reply['public'], reply['private']
        correct = verify_rsa(p, q, e, d)
        logging.info('p=%s prime=%s; q=%s prime=%s', p, is_prime(p), q, is_prime(q))
        logging.info('public=(%s, %s), private=(%s, %s), correct=%s', e, p*q, d, p*q, correct)
        if not correct:
            raise ValueError('incorrect RSA keypair')
        return correct
    expect(reply, 1, kind)
    if kind == 'RSA':
        n, e = reply['parameter']['n'], public_integer(reply['public'])
        if type(n) is not int or not 400**2 <= n <= 500**2 or not 1 < e < n:
            raise ValueError('invalid RSA public parameters')
        key = secrets.token_bytes(32)
        channel.send({'opcode': 2, 'type': 'RSA',
                      'encrypted_key': [pow(b, e, n) for b in key]})
    elif kind == 'DH':
        p, g, public = validate_dh(reply)
        private = dh_private(p)
        key = dh_aes_key(pow(public, private, p))
        channel.send({'opcode': 1, 'type': 'DH', 'public': pow(g, private, p)})
    else:
        raise ValueError('unknown protocol')
    plaintext = receive_aes(channel, key)
    send_aes(channel, key, message)
    return plaintext


def respond(channel, message, fault=None):
    request = channel.receive()
    kind = request.get('type')
    expect(request, 0, kind)
    if kind == 'RSAKey':
        p, q, e, d = rsa_keypair()
        channel.send({'opcode': 0, 'type': kind, 'private': d, 'public': e,
                      'parameter': {'p': p, 'q': q}})
        return True
    if kind == 'RSA':
        p, q, e, d = rsa_keypair()
        n = p * q
        channel.send({'opcode': 1, 'type': kind, 'public': e, 'parameter': {'n': n}})
        reply = expect(channel.receive(), 2, 'RSA')
        encrypted = reply['encrypted_key']
        if (not isinstance(encrypted, list) or len(encrypted) != 32
                or any(type(c) is not int or not 0 <= c < n for c in encrypted)):
            raise ValueError('invalid encrypted_key')
        values = [pow(c, d, n) for c in encrypted]
        if any(b > 255 for b in values):
            raise ValueError('invalid RSA-decrypted byte')
        key = bytes(values)
    elif kind == 'DH':
        p, g = dh_parameters()
        if fault == 'prime':
            p = 405
        elif fault == 'generator':
            g = 1
        private = dh_private(p)
        channel.send({'opcode': 1, 'type': kind, 'public': pow(g, private, p),
                      'parameter': {'p': p, 'g': g}})
        reply = expect(channel.receive(), 1, 'DH')
        public = public_integer(reply['public'])
        if not 1 <= public < p:
            raise ValueError('invalid DH public key')
        key = dh_aes_key(pow(public, private, p))
    else:
        raise ValueError('unknown protocol')
    send_aes(channel, key, message)
    return receive_aes(channel, key)


def session(sock, role, kind, message, fault=None):
    sock.settimeout(15)
    channel = Channel(sock)
    try:
        if role == 'initiator':
            return initiate(channel, kind, message)
        return respond(channel, message, fault)
    except RemoteError as exc:
        logging.error('Peer error: %s', exc)
        return False
    except (ValueError, KeyError, TypeError, OverflowError, OSError) as exc:
        error = str(exc) if isinstance(exc, ValueError) else 'invalid message or connection: ' + str(exc)
        logging.error('%s', error)
        try:
            channel.send({'opcode': 3, 'error': error})
        except OSError:
            pass
        return False
