import ast

res = {}
try:
    with open('../atom_wise_resolver/decisions', 'r') as f:
        try:
            content = f.read()
            dic = content.split('---')
            decisions = ast.literal_eval(dic[2])
            glossary = ast.literal_eval(dic[1])
        except:
            print('Content could not be translated to pure dictionary, contrary to expectation.')
except: 
    print('Error reading the output file. Maybe the previous program (DPLL) broke somewhere.')

resultStr = ''

for key in decisions:
    if decisions[key] == True:
        print(glossary[key-1])
