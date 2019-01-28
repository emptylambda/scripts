"""Query general consensus from competition result

Example:
        $ python3 query.py lia/chc-lia-0270.smt2

Todo:
    * looping
    * selection from all questions
    * detail reporting (i.e. sat: 4 (...solvers...)) 

""" 


import pandas as pd
import sys

# print('Python version' + sys.version)
# print('Pandas version' + pd.__version__)

location= r'../Job29664_info.csv'
df = pd.read_csv(location)

# solvers = df.groupby('solver')
# for qname, group in solvers:
#     print(qname)

def fecthQuestion(quest_no):
    questions = df.groupby('benchmark', as_index=False)
    for qname, group in questions:
        if qname == quest_no: 
            return group


if __name__ == '__main__':
    for qname in sys.argv[1:]:
        groupR = fecthQuestion(qname)
        if groupR is not None:
            resultCount = groupR['result'].value_counts()
            print(resultCount)
        else:
            print("Question " + qname + " not found")

