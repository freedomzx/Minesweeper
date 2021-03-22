from collections import deque
from environmentGenerator import *

def testone():
        nums = {}
        nums["flags"] = 0
        nums["totalQueries"] = 0
        testtwo(nums)
        print(nums)

def testtwo(nums):
        nums["flags"] += 1
        nums["totalQueries"] += 1

testone()