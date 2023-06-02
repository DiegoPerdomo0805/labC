#file = './tests/slr-1.yal'

from yalex import grammar, generate_alphabet, parser
from InfixToPostfix import *
from BinaryTree import *
import time

files = [
    #'./tests/slr-1.yal',
    './tests/slr-2.yal',
    './tests/slr-3.yal',
    './tests/slr-4.yal'
]

#file = files[1]


def main(file):
    print('-------------------------------------------------------------')    

    l, r = grammar(file)
    sigma, regex = generate_alphabet(l, r)

    print('Vex\'ahlia Vessar')
    print('-------------------------------------------------------------')


    for e in l:
        print(e, ' = ', l[e])

    print('Cassandra de Rolo')
    print('-------------------------------------------------------------')

    for e in r:
        print(e, ' = ', r[e])

    print('\nPercival Frederickstein von Musel Klossowski de Rolo III')
    print('-------------------------------------------------------------')


    print('Alfabeto: ', sigma)
    print('Expresion regular: ', regex)

    print('-------------------------------------------------------------')


    r, sigma = parser(regex, l, sigma)

    r_string = ''.join(r)

    #print('Array regex: ', r)
    print('Expresion regular: ', r_string)
    print('Keyleth')
    print('--------------------------------------------------------.-----')

    

    tratemos = InfixToPostfix(r)

    print('Expresion regular postfija: ', ''.join(tratemos))

    print('-'*60)

    

    tratemos.append('#')
    tratemos.append("'.'")

    tree = buildTree(tratemos.pop(), tratemos)

    visual_tree = tree.generate_graph()
    tree.traversePostOrder()
    #tree.post2()
    #tree.determineFollowPos()
    #tree.post3()
    print('-------------------------------------------------------------')

    visual_tree.render(file, view=True, format='png', cleanup=True, directory='./visual/', quiet=True)

for i in range(len(files)):
    print('Prueba ', i+1)
    main(files[i])
    # make the program wait for some seconds
    time.sleep(3)

#main(files[2])