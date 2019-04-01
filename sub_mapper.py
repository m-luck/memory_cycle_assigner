from sub_clausifier import *
import os

db: bool = False# Turn debug on or off

def generateClauses():
    try:
        path = sys.argv[1]
    except:
        print("Please input the path of the register requirements.") 
    else:
        reqs = p.read_in(path)
        start = reqs['START']
        goal = reqs['GOAL']
        limit = reqs['LIMIT']

        possasses = permute_possible_assignments(start)
        possvals = permute_possible_values(start)
        single_state = permute_single_state(start)

        lsva = [limit, start, possvals, possasses] # LSVA: Limit, Start, Values Possible, Assignments possible
        lsvamin1 = [limit-1, start, possvals, possasses]
        funlist = [clausified_uniqueness, clausified_incompatibility]
        funlistmin1 = [clausified_positivity, clausified_framing]
        clauses = permute_each_time_step(*lsva, funlist)
        clauses.extend(permute_each_time_step(*lsvamin1, funlistmin1))
        clauses.extend(clausifiedStart(limit, start, possvals, possvals))
        clauses.extend(clausifiedGoal(limit, start, possvals, possasses, goal))
        return clauses

def extractUniqueAtoms(clauses: List):
    distinct_atoms = {}
    atom_index = 1
    for clause in clauses: 
        for atom in clause[0]:
            atom = atom[1:]
            if str(atom) not in distinct_atoms:
                distinct_atoms[str(atom)] = atom_index
                atom_index += 1
                if db: print('Atom',atom_index,atom)
    return distinct_atoms

def convertClausesToGeneric(clauses: List, distinct_atoms: Dict):
    generic_clauses = {}
    for i, clause in enumerate(clauses):
        new_clause = []
        for atom in clause[0]:
            atomBool = atom[0]
            atomItself = atom[1:]
            if atomBool == 'NOT': new_clause.append([False,distinct_atoms[str(atomItself)]])
            else: new_clause.append([True,distinct_atoms[str(atomItself)]])
        generic_clauses[i] = new_clause
        if db: print('Gen Clause', i+1, new_clause, clause[2])
    return generic_clauses

def stringifyGenClausesToOutput(genericClauses: Dict):
    clauseStrings = []
    for i, key in enumerate(genericClauses):
        clause = genericClauses[key]
        line = []
        for atom in clause:
            atomBool = atom[0]
            atomID = atom[1]
            if atomBool is True: line.append(str(atomID)) 
            else: line.append('-'+str(atomID))
        line = join(line, ' ')
        clauseStrings.append(line)
    fullString = join(clauseStrings,'\n')
    if db: print(fullString)
    return fullString

def mapOutput():
    clauses = generateClauses()
    specificAtoms = extractUniqueAtoms(clauses)
    genericClauses = convertClausesToGeneric(clauses, specificAtoms)
    clauseStrings = stringifyGenClausesToOutput(genericClauses)
    atomDict = {}
    for i, atom in enumerate(specificAtoms): 
        atomDict[i] = atom
    atomStrings = join(specificAtoms, '\n')
    file = open('front_end_output', 'w+')
    file.write(clauseStrings + '\n0\n---' + str(atomDict))
    file.close()
    
if __name__ == "__main__":
    mapOutput()
