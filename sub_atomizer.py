from enum import Enum
from typing import Dict, List
import sub_parser as p
import sys
import textwrap

class Atom(Enum):
    VAL=0
    ASS=1

def clausify_single(atoms: List, booleanAss, reason):
    '''
    Takes a list of single atoms and establishes them all to a given truth value.
    They are singletons which we are batch-defining for ease of use.
    '''
    clausified = [] 
    for atom in atoms:
        fullAtom = [[booleanAss]+atom+['val']]
        clausified.append([fullAtom, reason])
    return clausified

def necessitate_truth(atoms: List, reason):
    '''
    All atoms in this list will always yearn to be true.
    '''
    return clausify_single(atoms, ' ', reason)

def necessitate_falsehood(atoms: List, reason):
    '''
    All atoms in this list will always yearn to be false.
    '''
    return clausify_single(atoms, 'NOT', reason)

def makeFullAtom(boolVal: bool, slot1, slot2, time: int, type: int):
    '''
    Makes creating atoms slightly faster.
    '''
    notStat = ' ' if bool else 'NOT'
    typeStr = 'val' if Atom.type.value==1 else 'ass'
    resList = [notStat, slot1, slot2, time, typeStr]

def atomized_uniqueness(value_atoms: List, values: List, time: int):
    '''
    Takes a set of established values and returns the values that cannot coexist with these.
    '''
    unique_val_nots = []
    for i, atom in enumerate(value_atoms):
        for i, val in enumerate(values):
            if atom[1]!=val:
                unique_val_nots.append([atom[0],val,time])
    return unique_val_nots

def atomized_state(state: Dict, time: int):
    '''
    Takes a state and returns the next values in a tuple along with the values that cannot coexist.
    '''
    value_atoms = []
    values = []
    for i, key in enumerate(state):
        value_atoms.append([key, state[key], time])
        values.append(state[key])
    unique_val_nots = atomized_uniqueness(value_atoms, values, time)
    return value_atoms, unique_val_nots
    

def populateStartGoal(reqs: Dict):
    start, antistart = atomized_state(reqs['START'], 0)
    goal, antigoal = atomized_state(reqs['GOAL'], reqs['LIMIT'])
    clausified = necessitate_truth(start+goal, 'want true') + necessitate_falsehood(antistart+antigoal, 'want false') 
    return clausified 

def printClauses(clauses: List, preferredWidth = 70):
    for i, clause in enumerate(clauses):
        prefix = "Clause "+str(i+1)+"\t"
        wrapper = textwrap.TextWrapper(initial_indent=prefix, width=preferredWidth,
                            subsequent_indent=' '*len(prefix))
        message = wrapper.fill(str(clause[1])+"\t"+str(clause[0]))
        print(message)

if __name__ == "__main__":
    try:
        path = sys.argv[1]
    except:
        print("Please input the path of the register requirements.") 
    else:
        reqs = p.read_in(path)
        clauses = populateStartGoal(reqs)
        printClauses(clauses)
