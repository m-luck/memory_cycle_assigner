from enum import Enum
from typing import Dict, List
from sub_atomizer import *

def permute_possible_assignments(start: Dict, time: int):
    possibleAssignments = []
    for i, assignTo in enumerate(start):
        for j, assignFrom in enumerate(start):
            if assignTo != assignFrom:
                possibleAssignments.append([assignTo, assignFrom, time])
    return possibleAssignments

def permute_in_time_step(time: int):
    pass

def clausified_positivity(asstuple: List, initState: Dict):
    '''
    (Ass(RA,RB,I)^Val(RB,Vb,I)) -> Val(RA,Vb,I+1) 
    == XAss v XVal v Val [via DeMorgans and implication removal]
    '''
    afterstate = []
    writeToRA = asstuple[0]
    writeFromRB = asstuple[1]
    atTimeI = asstuple[2]
    Vb = initState[writeFromRB]
    XAss = makeFullAtom(False, writeToRA, writeFromRB, atTimeI, ASS)
    XVal = makeFullAtom(False, writeFromRB, Vb, atTimeI, VAL)
    Val = makeFullAtom(True, writeToRA, Vb, atTimeI+1, VAL)
    return [[XAss, XVal, Val], 'positivity']

def permute_positivity(a):
    pass

def clausified_framing(val: List, state: Dict, time: int): 
    '''
    Frame axiom (no change if no assignment) 
    If Value(R,Vx,I) and not Assign(R,R1,I) and not Assign(R,R2,I) and ... and not Assign(R,Rn,I) then Value(R,Vx,I+1)
    = [Val(R,Vx,I) ^ (XAss(R,Rn,I) [for Rn in all R]) => Val(R, Vx, I+1)
    = X[...] ^ Val(R, Vx, I+1)
    = [XVal(R,Vx,I) v (Ass(R,Rn,I) [for Rn in all R]) v Val(R, Vx, I+1)
    '''
    # for reg in state:
    # XVal = makeFullAtom(False, Ra, Va, I)
    pass


if __name__ == "__main__":
    try:
        path = sys.argv[1]
    except:
        print("Please input the path of the register requirements.") 
    else:
        reqs = p.read_in(path)
        res = permute_possible_assignments(reqs['START'], 1)
        print(res)