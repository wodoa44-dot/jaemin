import argparse
import logging

def command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--first", metavar="<number A>", help="Value for the number A", type=int, required=True)
    parser.add_argument("-b", "--second", metavar="<number B>", help="Value for the number B", type=int, required=True)
    parser.add_argument("-l", "--log", metavar="<log level>", help="Log level (DEBUG/INFO/WARNING/ERROR/CRITICAL)", type=str)
    args = parser.parse_args()
    return args

def main():
    args = command_line_args()
    logLevel = args.log
    logging.basicConfig(level=logLevel)

    logging.info("Start the application")
    logging.debug("The first argument: {}".format(args.first))
    logging.debug("The second argument: {}".format(args.second))
    logging.info("Sum of the two numbers: {}".format(args.first + args.second))

if __name__ == "__main__":
    main()
