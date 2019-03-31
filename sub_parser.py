from enum import Enum
from typing import List
import ast
import os
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

def read_dpll_out(path=os.path.join(os.pardir, 'decisions')):
    with open(path, 'r') as f:
        content = f.readlines()
        pairs = {}
        for line in content:
            if line[0] =='0': break
            else:
                chars = re.split(" |\t|\r|\n", line) 
                singlePair = populatePairs(chars)
                pairs.update(singlePair)
    return pairs

 
def read_glossary(path=os.path.join(os.pardir, 'front_end_output')):
    glossary = None
    try:
        with open(os.path.join(os.pardir, 'decisions'), 'r') as f:
            try:
                content = f.read()
                dic = content.split('---')
                glossary = ast.literal_eval(dic[1])
            except:
                print('Content could not be translated to pure dictionary, contrary to expectation.')
    except: 
        print('Error reading the output file. Maybe the previous program (DPLL) broke somewhere.')
    return glossary

def strToList(str):
    res = ast.literal_eval(str)
    assert isinstance(res, list) 
    return res

if __name__ == "__main__":
    try:
        path = sys.argv[1]
    except:
        print("Please input the path of the register requirements.") 
    else:
        print(read_in(path))