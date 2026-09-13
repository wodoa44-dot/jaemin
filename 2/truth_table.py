import re
import argparse
import logging
import copy
import time
from operators import *

def extract_variables(expression):
    sorted_variable_set = sorted(set(re.findall(r'\b[a-z]\b', expression)))
    return sorted_variable_set

def combination(nvar):
    if nvar == 1:
        return [[True], [False]]
    else:
        comb = combination(nvar-1)
        ret = []
        for c in comb:
            c1 = copy.copy(c)
            c1.append(True)
            c2 = copy.copy(c)
            c2.append(False)
            ret.append(c1)
            ret.append(c2)
        return ret


def truth_table(expression):
    variables = extract_variables(expression)
    nvar = len(variables)
    ret = combination(nvar)

    for c in ret:
        idx = 0
        for v in variables:
            exec("{}={}".format(v, c[idx]))
            idx += 1
        val = eval(expression)
        c.append(val)
    
    return ret

def print_truth_table(expression):
    table = truth_table(expression)
    variables = extract_variables(expression)
    nvars = len(variables)

    print("|", end="")
    for v in variables:
        print ("\t{}\t|".format(v), end="")
    print("\t{}\t|".format(expression))
    for r in table:
        print("|", end="")
        for e in r:
            print("\t{}\t|".format(e), end="")
        print("")

def command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--exp", required=True, help="Expression", type=str)
    parser.add_argument("-l", "--log", help="Log level (DEBUG/INFO/WARNING/ERROR/CRITICAL)", type=str, default="INFO")

    args = parser.parse_args()
    return args

def main():
    args = command_line_args()
    logging.basicConfig(level=args.log)

    logging.info("Expression: {}".format(args.exp))
    logging.debug("  Extracted variables: {}".format(extract_variables(args.exp)))
    print_truth_table(args.exp)

if __name__ == "__main__":
    main()
