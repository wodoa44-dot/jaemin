import argparse
import logging

def command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--min", help="Minimum value of the solution range", type=int, default=-100)
    parser.add_argument("-n", "--max", help="Maximum value of the solution range", type=int, default=100)
    parser.add_argument("-l", "--log", help="Log level (DEBUG/INFO/WARNING/ERROR/CRITICAL)", type=str, default="INFO")
    args = parser.parse_args()
    return args

def main():
    args = command_line_args()
    logging.basicConfig(level=args.log)

    r = range(args.min, args.max)
    solutions = []

    # TODO: find the solutions of the equation x^2 - 100x + 1600 = 0
    for x in range(-100, 100):
        if x*x - 100*x + 1600 == 0:
            solutions.append(x)

    logging.info("Solutions: {}".format(solutions))

if __name__ == "__main__":
    main()
