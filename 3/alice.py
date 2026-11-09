import argparse
import logging
import socket
from protocol import session


def run(addr, port, protocol='DH', message='world', role='initiator'):
    with socket.create_connection((addr, port), timeout=15) as conn:
        logging.info('Alice is connected to %s:%s', addr, port)
        return session(conn, role, protocol, message)


def command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--addr', required=True)
    parser.add_argument('-p', '--port', type=int, required=True)
    parser.add_argument('-l', '--log', default='INFO')
    parser.add_argument('-t', '--protocol', choices=['RSAKey', 'RSA', 'DH'], default='DH')
    parser.add_argument('-m', '--message', default='world')
    parser.add_argument('--role', choices=['initiator', 'responder'], default='initiator')
    return parser.parse_args()


def main():
    args = command_line_args()
    logging.basicConfig(level=args.log.upper())
    try:
        result = run(args.addr, args.port, args.protocol, args.message, args.role)
    except OSError as exc:
        logging.error('%s', exc)
        raise SystemExit(1)
    if result is False:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
