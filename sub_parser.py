from enum import Enum
from typing import List
import sys
import re

class Row(Enum):
    START = 0
    GOAL = 1
    LIMIT = 2
    
def populatePairs(chars: List[str]):
    res = {}
    for i, char in enumerate(chars):
        if char.isalnum() and i % 2 == 0:
            try:
                res[int(char)] = chars[i+1]
            except:
                print("There seems to be an unpaired item.")
    return res

def read_in(filePath: str):
    start = {}
    goal = {}
    limit = 0
    row = -1
    with open(filePath, "r") as file:
        for line in file:
            chars = re.split(" |\t|\r|\n", line) 
            if chars[0].isalnum():
                row += 1
            if row==Row.START.value:
                start = populatePairs(chars)
            elif row==Row.GOAL.value:
                goal = populatePairs(chars)
            elif row==Row.LIMIT.value:
                for char in chars:
                    if char.isdigit():
                        limit = int(char) 
                        break
                else: 
                    print("Could not find step limit.")
    requirements = {}
    requirements['START'], requirements['GOAL'], requirements['LIMIT'] = start, goal, limit
    return requirements

if __name__ == "__main__":
    try:
        path = sys.argv[1]
    except:
        print("Please input the path of the register requirements.") 
    else:
        print(read_in(path))