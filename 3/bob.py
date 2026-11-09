import argparse
import logging
import socket
import threading
from protocol import session


def handler(sock, message='hello', role='responder', protocol='DH', fault=None):
    with sock:
        return session(sock, role, protocol, message, fault)


def run(addr, port, message='hello', role='responder', protocol='DH', fault=None, once=False):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as bob:
        bob.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        bob.bind((addr, port))
        bob.listen(10)
        logging.info('Bob is listening on %s:%s', addr, port)
        while True:
            conn, info = bob.accept()
            logging.info('Bob accepts %s:%s', *info)
            if once:
                return handler(conn, message, role, protocol, fault)
            threading.Thread(target=handler,
                             args=(conn, message, role, protocol, fault), daemon=True).start()


def command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--addr', default='0.0.0.0')
    parser.add_argument('-p', '--port', type=int, required=True)
    parser.add_argument('-l', '--log', default='INFO')
    parser.add_argument('-m', '--message', default='hello')
    parser.add_argument('-t', '--protocol', choices=['RSAKey', 'RSA', 'DH'], default='DH')
    parser.add_argument('--role', choices=['initiator', 'responder'], default='responder')
    parser.add_argument('--fault', choices=['prime', 'generator'])
    parser.add_argument('--once', action='store_true')
    return parser.parse_args()


def main():
    args = command_line_args()
    logging.basicConfig(level=args.log.upper())
    try:
        result = run(args.addr, args.port, args.message, args.role,
                     args.protocol, args.fault, args.once)
    except OSError as exc:
        logging.error('%s', exc)
        raise SystemExit(1)
    if result is False:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
