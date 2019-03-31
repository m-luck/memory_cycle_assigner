import sub_parser as p
from sub_atomizer import join

def printFullRender(start, goal, k, solution):
    if len(solution) == 0: fullPrint = 'No Solution.'
    else:
        print("Let's solve this real world problem using resolution!")
        startLine = 'Start: '
        startRegs = join(start, ', ')
        startLine += startRegs + '.'
        fullPrint = startLine + "\n"
        goalLine = 'End: '
        goalRegs = join(goal, ', ')
        goalLine += goalRegs + '.'
        fullPrint += goalLine + '\n'
        fullPrint += "K = " + str(k) + '\n\nSolution:'
        for cycle in solution:
            cycleAss = join(solution[cycle], ', ')        
            fullPrint += '\nCycle ' + str(cycle+1) + ": " + cycleAss + '.'
    print(fullPrint)


glossary = p.read_glossary()
decisions = p.read_dpll_out()
trueAtoms = []
for key in decisions:
    if decisions[key] == 'T':
        trueAtoms.append(glossary[key-1])

trueAtoms = list(map(lambda x: p.strToList(x), trueAtoms))
trueAtoms = sorted(trueAtoms, key=lambda x: x[4], reverse=True)
sortedAtoms = sorted(trueAtoms, key=lambda x: x[3])

solutionStr = ''
valueTups = {}
start = []
goal = []
solution = {}
k = -1
for atom in sortedAtoms: 
    atomTime = atom[3]
    if atomTime > k:
        k = atomTime
for atom in sortedAtoms:
    atomType = atom[4]
    atomTime = atom[3]
    if atomType == 'val':
        R = atom[0]
        Rval = atom[1]
        addStr = \
            'Value(' + \
            str(R) + ',' + \
            str(Rval) + ',' + \
            str(atomTime) + \
            ')\n'
        if addStr not in valueTups: # prevent redudant atoms
            valueTups[addStr] = 1
            solutionStr += addStr
            if atomTime == 0:
                start.append('R{R} = {Rval}'.format(R=R, Rval=Rval))
            elif atomTime == k:
                goal.append('R{R} = {Rval}'.format(R=R, Rval=Rval))
    elif atomType == 'ass':
        Rto = atom[0]
        Rfrom = atom[2]
        if Rto != Rfrom: # remove self assignment
            solutionStr += \
                'Assignment(' + \
                str(Rto) + ',' + \
                str(Rfrom) + ',' + \
                str(atomTime) + \
                ')\n'
            currentSol = solution.get(atomTime, [])
            currentSol.append('R{Ra} = R{Rb}'.format(Ra=Rto, Rb=Rfrom))
            solution.update({atomTime: currentSol})
    
printFullRender(start, goal, k, solution)         
            

