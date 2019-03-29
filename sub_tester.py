from sub_clausifier import *

def test_uniqueness_population(limit, start, possvals, possasses):
    uniqueness_clauses = permute_each_time_step(limit, start, possvals, possasses, [clausified_uniqueness])
    printClauses(uniqueness_clauses)

def test_positivity_population(limit, start, possvals, possasses):
    pass

def test_framing_population(limit, start, possvals, possasses):
    pass

if __name__ == "__main__":
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
        lsva = [limit, start, possvals, possasses] # LSVA: Limit, Start, Values Possible, Assignments possible

        print("Poss Vals:",possvals,'\n')
        print("Poss Asses:",possasses,'\n')

        test_uniqueness_population(*lsva)
        test_positivity_population(*lsva)