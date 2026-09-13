import argparse
import logging
from operators import *

def command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--p-value", required=True, help="Boolean value of p", type=str, choices=["True", "False"])
    parser.add_argument("-q", "--q-value", required=True, help="Boolean value of q", type=str, choices=["True", "False"])
    parser.add_argument("-e", "--exp", required=True, help="Expression", type=str)
    parser.add_argument("-l", "--log", help="Log level (DEBUG/INFO/WARNING/ERROR/CRITICAL)", type=str, default="INFO")

    args = parser.parse_args()
    return args

def main():
    args = command_line_args()
    logging.basicConfig(level=args.log)

    e = "p={}".format(args.p_value)
    logging.debug(e)
    exec(e)
    e = "q={}".format(args.q_value)
    logging.debug(e)
    exec(e)
    ret = eval(args.exp)
    logging.info("{} is {}".format(args.exp, ret))

if __name__ == "__main__":
    main()
