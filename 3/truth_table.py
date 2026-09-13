import re
import argparse
import logging
import copy
import time
from operators import *

def extract_variables(expression):
    sorted_variable_set = sorted(set(re.findall(r'\b[a-z]\b', expression)))
    return sorted_variable_set

def truth_table(expression):
    vlst = extract_variables(expression)
    combinations = []

    start = time.time()
    for _ in range(len(vlst)):
        if combinations == []:
            combinations = [[True], [False]]
        else:
            tmp = copy.copy(combinations)
            combinations = []
            for c in tmp:
                e1 = copy.copy(c)
                e1.append(True)
                combinations.append(e1)
                e2 = copy.copy(c)
                e2.append(False)
                combinations.append(e2)

    for c in combinations:
        for i in range(len(vlst)):
            exec("{}={}".format(vlst[i], c[i]))
        ret = eval(expression)
        c.append(ret)
    end = time.time()

    #print ("elapsed time: {} second".format(end - start))
    return combinations

def print_truth_table(expression):
    t = truth_table(expression)
    vlst = extract_variables(expression)

    print ("|\t", end="")
    for v in vlst:
        print ("{}\t|".format(v), end="")
    print ("{}\t|".format(expression))

    for r in t:
        print ("|\t", end="")
        for e in r:
            print ("{}\t|".format(e), end="")
        print ("")

def count_satisfying(expression):
    table = truth_table(expression)
    ret = 0

    for r in table:
        if r[-1] == True:
            ret += 1

    return ret

def is_tautology(expression):
    table = truth_table(expression)
    ret = True
    for r in table:
        if r[-1] == False:
            ret = False
            break
    return ret

def are_equivalent(exp1, exp2):
    table1 = truth_table(exp1)
    table2 = truth_table(exp2)
    ret = True

    if len(table1) != len(table2):
        ret = False
    else:
        for i in range(len(table1)):
            if table1[i][-1] != table2[i][-1]:
                ret = False
                break
    return ret

def command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--exp1", required=True, help="Expression 1", type=str)
    parser.add_argument("-f", "--exp2", help="Expression 2", type=str)
    parser.add_argument("-l", "--log", help="Log level (DEBUG/INFO/WARNING/ERROR/CRITICAL)", type=str, default="INFO")

    args = parser.parse_args()
    return args

def main():
    args = command_line_args()
    logging.basicConfig(level=args.log)

    if args.exp2:
        logging.info("Expression 1: {}".format(args.exp1))
        logging.debug("  Extracted variables 1: {}".format(extract_variables(args.exp1)))
        logging.info("Expression 2: {}".format(args.exp2))
        logging.debug("  Extracted variables 2: {}".format(extract_variables(args.exp2)))
        logging.info("Two expressions are equivalent: {}".format(are_equivalent(args.exp1, args.exp2)))
    else:
        logging.info("Expression: {}".format(args.exp1))
        logging.debug("  Extracted variables: {}".format(extract_variables(args.exp1)))
        logging.info("The number of combintations that satisfy the expression: {}".format(count_satisfying(args.exp1)))
        logging.info("The expression is tautology: {}".format(is_tautology(args.exp1)))

if __name__ == "__main__":
    main()
