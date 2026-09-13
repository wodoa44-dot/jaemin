import re
import argparse
import logging
import copy
import time
from operators import *

# TODO: the function checks if a predicate p is true for all elements in U
def is_true_for_all(p, u):
    ret = True
    for i in u:
        exec("x = {}".format(i))
        r = eval(p)
        if r == False:
            ret = False
            break
    return ret

# TODO: the function checks if a predicate p is true for some elements in U
def exists_for_some(p, u):
    ret = False
    for i in u:
        exec("x = {}".format(i))
        r = eval(p)
        if r == True:
            ret = True
            break
    return ret

# TODO: the function checks if a predicate p is true for all elements of all domains
def is_valid(p, ulst):
    ret = True
    for u in ulst:
        if is_true_for_all(p, u) == False:
            ret = False
            break
    return ret

# TODO: the function checks if a predicate p is true for some elements of some domains
def is_satisfiable(p, ulst):
    ret = False
    for u in ulst:
        if exists_for_some(p, u) == True:
            ret = True
            break
    return ret

# TODO: the function checks if two predicates are logically equivalent
def are_equivalent(p1, p2, ulst):
    ret = True
    for u in ulst:
        p12 = "{} |iff| {}".format(p1, p2)
        if not is_true_for_all(p12, u):
            ret = False
            break
    return ret

def command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--u1", required=True, nargs="+", help="Elements of Domain 1", type=int)
    parser.add_argument("-v", "--u2", nargs="+", help="Elements of Domain 2", type=int)
    parser.add_argument("-a", "--p1", required=True, help="Predicate 1", type=str)
    parser.add_argument("-b", "--p2", help="Predicate 2", type=str)
    parser.add_argument("-q", "--q1", help="Nested Quantifier 1", type=str, choices=["universal", "existential"])
    parser.add_argument("-r", "--q2", help="Nested Quantifier 2", type=str, choices=["universal", "existential"])
    parser.add_argument("-l", "--log", help="Log level (DEBUG/INFO/WARNING/ERROR/CRITICAL)", type=str, default="INFO")

    args = parser.parse_args()
    return args

def main():
    args = command_line_args()
    logging.basicConfig(level=args.log)

    logging.debug("Domain 1: {}".format(args.u1))
    logging.debug("Domain 2: {}".format(args.u2))
    ulst = []
    ulst.append(args.u1)
    ulst.append(args.u2)

    if args.p2:
        logging.info("Predicate 1: {}".format(args.p1))
        logging.info("Predicate 2: {}".format(args.p2))
        logging.info("Two predicates are equivalent: {}".format(are_equivalent(args.p1, args.p2, ulst)))
    elif args.u2:
        logging.info("Predicate: {}".format(args.p1))
        logging.info("The predicate is valid: {}".format(is_valid(args.p1, ulst)))
        logging.info("The predicate is satisfiable: {}".format(is_satisfiable(args.p1, ulst)))
    else:
        logging.info("Predicate: {}".format(args.p1))
        logging.info("The predicate is true for all elements in {}: {}".format(args.u1, is_true_for_all(args.p1, args.u1)))
        logging.info("The predicate is true for some elements in {}: {}".format(args.u1, exists_for_some(args.p1, args.u1)))

if __name__ == "__main__":
    main()
