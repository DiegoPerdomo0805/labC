#file = './tests/slr-1.yal'

from yalex import grammar, generate_alphabet, parser, PreprocessEntry, updateSigma
from InfixToPostfix import *
from BinaryTree import *
import time
from AFN_to_AFD import *
from AFN import *
from direct_AFD import *
from mini import *
from lr import *

files = [
    './tests/slr-1.yal',
    './tests/slr-2.yal',
    './tests/slr-3.yal',
    './tests/slr-4.yal'
]

yalps = [
    './tests/slr-1.yalp',
    './tests/slr-2.yalp',
    './tests/slr-3.yalp',
    './tests/slr-4.yalp'
]


#file = files[1]

def visual_automatas(AFD_D_min, regex):
    Minimizacion_Visual(AFD_D_min, 'AFD directo' , ''.join(regex))


def automatas(tree, postfix, sigma):
    AFD_directo = direct_build(tree, sigma, postfix)
    #Minimizacion_Visual(AFD_min, 'AFN a AFD', ''.join(regex))
    AFD_D_min = Minimization(AFD_directo, sigma)

    return AFD_D_min

def writeLog(bitacora, nombre):
    with open(nombre, 'w', encoding='utf-8') as f:
        f.write(bitacora)

def main(file, yalp):
    print('-------------------------------------------------------------')    

    l, r = grammar(file)
    sigma, regex = generate_alphabet(l, r)

    print('-------------------------------------------------------------')


    for e in l:
        print(e, ' = ', l[e])

    print('-------------------------------------------------------------')

    for e in r:
        print(e, ' = ', r[e])

    print('\nPercival Frederickstein von Musel Klossowski de Rolo III')
    print('-------------------------------------------------------------')


    exp, sigma = parser(regex, l, sigma)

    r_string = ''.join(exp)

    #print('Array regex: ', r)
    print('Expresion regular: ', r_string)
    print('-------------------------------------------------------------')

    

    tratemos = InfixToPostfix(exp)
    postfix_copia = tratemos.copy()
    updateSigma(exp, sigma)

    print('Expresion regular postfija: ', ''.join(tratemos))
    print('Alfabeto: ', sigma)

    print('-'*60)

    

    tratemos.append('#')
    tratemos.append("'.'")

    tree = buildTree(tratemos.pop(), tratemos)
    # #visual_tree = tree.generate_graph()
    # tree.traversePostOrder()
    # tree.determineFollowPos()
    # AFD_D_min = automatas(tree, postfix_copia, sigma)
    # #visual_automatas(AFD_D_min, regex)


    """dummy = "     8.9E-12"
    print(dummy)

    dummy, aver = PreprocessEntry(dummy, sigma)

    print(dummy)

    valid = "La cadena es valida" if aver else "La cadena no es valida"
    print(valid)"""
    print('-------------------------------------------------------------')
    
    
    

    tokens, productions = scan_tokens(yalp, r)

    print('Tokens: ', tokens)
    print('Producciones: ', productions)
    print('-------------------------------------------------------------')

    ini = startingPoint(productions)
    prod = ini
    ini += "'"
    #productions[ini][0] = '.' + prod
    productions[ini] = []
    productions[ini].append('.' + prod)
    print('Tokens: ', tokens)
    print('Producciones: ', productions)
    print('-------------------------------------------------------------')
    print(' - ', ini)
    print(' - ', productions)

    starter = create_state(productions, ini)
    print(' - ', starter)
    print(' - ', starter.name)
    print(' - ', starter.transitions)
    print(' - ', starter.contains)
    print(' - ', starter.isAccept)
    print(' - ', starter.isInitial)
    print(' - ' * 25)

    #aleluya = create_state(productions, ini)
    #print(' - ', aleluya)
    #print(' - ', aleluya.name)
    #print(' - ', aleluya.transitions)
    #print(' - ', aleluya.contains)
    #print(' - ', aleluya.isAccept)
    #print(' - ', aleluya.isInitial)
    #print(' - ' * 25)
    #states = []
    #generate_LR0_automaton(productions, aleluya, states)

    """states = process_states_and_transitions(tokens, productions, ini)

    for e in states:
        print(' - ', e.name)
        print(' - ', e.transitions)
        print(' - ', e.contains)
        print(' - ', e.isAccept)
        print(' - ', e.isInitial)
        print(' - ' * 25)"""

    print('-------------------------------------------------------------')


                

    #dummy = generate_LR0_automaton(tokens, productions)



    #pruebas = []
    """bitacora = ""
    bitacora += 'Expresion regular: ' + r_string + '\n'
    # leer archivo de pruebas tests.txt
    with open('./tests.txt', 'r', encoding='utf-8') as f:
        for line in f:
            #pruebas.append(line)
            line = line.strip()
            AFD_D_M_result, b = minimizedSimulation(AFD_D_min, line)
            bitacora += 'Cadena: ' + line + '\n'
            bitacora += b + '\n'
            bitacora += 'AFD directo minimizado: ' + str(AFD_D_M_result) + '\n'

    writeLog(bitacora, 'bitacora.txt')
    print(bitacora)"""

    print('-------------------------------------------------------------')


 #visual_tree.render(file, view=True, format='png', cleanup=True, directory='./visual/', quiet=True)



# for i in range(len(files)):
#     print('Prueba ', i+1)
#     main(files[i])
#     # make the program wait for some seconds
#     time.sleep(3)

which = 2
main(files[which], yalps[which])