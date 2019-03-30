from sub_clausifier import *

def test_single_generator(limit, start, possvals, possasses, fun):
    clauses = permute_each_time_step(limit, start, possvals, possasses, [fun])
    printClauses(clauses)

def test_uniqueness(limit, start, possvals, possasses):
    test_single_generator(limit, start, possvals, possasses, clausified_uniqueness)

def test_positivity(limit, start, possvals, possasses):
    test_single_generator(limit-1, start, possvals, possasses, clausified_positivity)

def test_framing(limit, start, possvals, possasses):
    test_single_generator(limit-1, start, possvals, possasses, clausified_framing)

def test_incompatibility(limit, start, possvals, possasses):
    test_single_generator(limit, start, possvals, possasses, clausified_incompatibility)

def test_all_clausifiers(limit, start, possvals, possasses):
    lsva = [limit, start, possvals, possasses]
    funlist = [clausified_uniqueness, clausified_incompatibility]
    clauses = permute_each_time_step(*lsva, funlist)

    lsva = [limit-1, start, possvals, possasses]
    funlist = [clausified_positivity, clausified_framing]

    clauses.extend(permute_each_time_step(*lsva, funlist))

    printClausesSimple(clauses)

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
        single_state = permute_single_state(start)

        lsva = [limit, start, possvals, possasses] # LSVA: Limit, Start, Values Possible, Assignments possible

        print("Poss Vals:",possvals,'\n')
        print("Poss Asses:",possasses,'\n')
        print("Poss States:",single_state)

        # test_uniqueness(*lsva)
        # test_positivity(*lsva)
        # test_framing(*lsva)
        # test_incompatibility(*lsva)
        test_all_clausifiers(*lsva)