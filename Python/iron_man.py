"""
@author: Askr-ssy
"""
import sys
import argparse
import time
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-env',dest="env",default="local")

args = parser.parse_args()
print(args.env,type(args.env))
time.sleep(10)
print("I am ")
print(__file__)
if args.env == "4":
    print("bingo")
    time.sleep(100)
    while True:
        time.sleep(1)
print(sys.argv)
