import argparse
import logging

def command_line_args():
    parser = argparse.ArgumentParser()
    # TODO: add options to get the unlimited number of elements of a list
    parser.add_argument("-n", "--num", help="Arguments", type=int, required=True, nargs="+")
    parser.add_argument("-l", "--log", help="Log level (DEBUG/INFO/WARNING/ERROR/CRITICAL)", type=str, default="INFO")
    args = parser.parse_args()
    return args

def main():
    args = command_line_args()
    logging.basicConfig(level=args.log)

    # TODO: fix the followings
    lst = args.num
    logging.info("Result: {}".format(sum(lst)))

if __name__ == "__main__":
    main()
