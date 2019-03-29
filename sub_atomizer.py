from enum import Enum
from typing import Dict, List
import sub_parser as p
import sys
import textwrap

class Atom(Enum):
    VAL=0
    ASS=1

def makeFullAtom(boolVal: bool, slot1, slot2, extraInfo, time: int, type):
    '''
    Makes creating atoms slightly faster.
    '''
    notStat = ' ' if boolVal else 'NOT'
    typeStr = 'ass' if type.value==1 else 'val'
    resList = [notStat, slot1, slot2, extraInfo, time, typeStr]
    return resList

def join(l, sep):
    '''
    Used in printClauses to join atoms in CNF clauses with the OR operator 'v'
    '''
    out_str = ''
    for i, el in enumerate(l):
        out_str += '{}{}'.format(el, sep)
    return out_str[:-len(sep)]

def printClauses(clauses: List, preferredWidth = 140):
    '''
    Prints a line with the Clause #, CNF clause, and meaning (for sanity)
    '''
    for i, clause in enumerate(clauses):
        prefix = "Clause "+str(i+1)+"\t"
        wrapper = textwrap.TextWrapper(initial_indent=prefix, width=preferredWidth,
                            subsequent_indent=' '*len(prefix))
        clauseItself = clause[0]
        clauseMeaning = clause[1]
        clauseCNF = join(clauseItself, " v ")
        message = wrapper.fill(clauseCNF+"\t"+str(clauseMeaning))
        print(message+"\n")

def permute_possible_values(start: Dict):
    '''
    Returns a general list of all assignments that can be at a register at a given time.
    In the format of a tuple (Register, Value, Start Register that held that value)
    This is basically all possible value atoms at a given time. 
    '''
    possible_values = []
    for i, reg in enumerate(start):
        extendBy = [(reg, start[origReg], origReg) for j, origReg in enumerate(start)]
        possible_values.extend(extendBy)
    return possible_values

def permute_possible_assignments(start: Dict):
    '''
    Likewise, all possible assignment atoms at a given time.
    '''
    possibleAssignments = []
    for i, assignTo in enumerate(start):
        for j, assignFrom in enumerate(start):
            # if assignTo != assignFrom: # If we want to prevent tautological assignments
            if True:
                possibleAssignments.append((assignTo, assignFrom))
    return possibleAssignments

if __name__ == "__main__":
    try:
        path = sys.argv[1]
    except:
        print("Please input the path of the register requirements.") 
    else:
        pass