import argparse
import logging

def load_elements(fname):
    lst = []
    with open(fname, "r") as f:
        for line in f:
            lst.append(line.strip())
    return lst

def remove_duplicates(lst):
    ret = []
    for x in lst:
        if x not in ret:
            ret.append(x)
    return ret

def command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--elements", required=True, help="File of Elements", type=str)
    parser.add_argument("-l", "--log", help="Log level (DEBUG/INFO/WARNING/ERROR/CRITICAL)", type=str, default="INFO")

    args = parser.parse_args()
    return args

def main():
    args = command_line_args()
    logging.basicConfig(level=args.log)

    lst = load_elements(args.elements)

    logging.info("# of elements in the list before removing duplicated elements: {}".format(len(lst)))
    logging.info("# of elements in the list after removing duplicated elements: {}".format(len(remove_duplicates(lst))))

if __name__ == "__main__":
    main()
