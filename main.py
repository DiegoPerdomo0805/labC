#file = './tests/slr-1.yal'

from yalex import grammar, generate_alphabet, parser, PreprocessEntry, updateSigma
from InfixToPostfix import *
from BinaryTree import *
import time
from AFN_to_AFD import *
from AFN import *
from direct_AFD import *
from mini import *

files = [
    './tests/slr-1.yal',
    './tests/slr-2.yal',
    './tests/slr-3.yal',
    './tests/slr-4.yal'
]

#file = files[1]

def visual_automatas(NFA, DFA_from_NFA, AFD_directo, AFD_min, AFD_D_min, regex):
    visual_AFN(NFA, ''.join(regex))
    visual_AFD_from_AFN(DFA_from_NFA, ''.join(regex))
    visual_directAFD(AFD_directo, ''.join(regex))
    Minimizacion_Visual(AFD_min, 'AFN a AFD', ''.join(regex))
    Minimizacion_Visual(AFD_D_min, 'AFD directo' , ''.join(regex))


def automatas(tree, postfix, sigma, regex):
    NFA = generateAFN(postfix)
    #visual_AFN(NFA, ''.join(regex))
    DFA_from_NFA = AFD_from_AFN(NFA, sigma)
    #visual_AFD_from_AFN(DFA_from_NFA, ''.join(regex))
    AFD_directo = direct_build(tree, sigma, postfix)
    #visual_directAFD(AFD_directo, ''.join(regex))
    AFD_min = Minimization(DFA_from_NFA, sigma)
    #Minimizacion_Visual(AFD_min, 'AFN a AFD', ''.join(regex))
    AFD_D_min = Minimization(AFD_directo, sigma)
    #Minimizacion_Visual(AFD_D_min, 'AFD directo' , ''.join(regex))

    #visual_automatas(NFA, DFA_from_NFA, AFD_directo, AFD_min, AFD_D_min, regex)

    return NFA, DFA_from_NFA, AFD_directo, AFD_min, AFD_D_min

def writeLog(bitacora, nombre):
    with open(nombre, 'w', encoding='utf-8') as f:
        f.write(bitacora)

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
    postfix_copia = tratemos.copy()
    updateSigma(r, sigma)

    print('Expresion regular postfija: ', ''.join(tratemos))
    print('Alfabeto: ', sigma)

    print('-'*60)

    

    tratemos.append('#')
    tratemos.append("'.'")

    tree = buildTree(tratemos.pop(), tratemos)

    #visual_tree = tree.generate_graph()
    
    tree.traversePostOrder()
    
    ########tree.post2()
    
    tree.determineFollowPos()
    
    ########tree.post3()
    #print(r)

    """dummy = "     8.9E-12"
    print(dummy)

    dummy, aver = PreprocessEntry(dummy, sigma)

    print(dummy)

    valid = "La cadena es valida" if aver else "La cadena no es valida"
    print(valid)"""
    
    NFA, DFA_from_NFA, AFD_directo, AFD_min, AFD_D_min = automatas(tree, postfix_copia, sigma, regex)

    #pruebas = []
    bitacora = ""
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
    print(bitacora)

    print('-------------------------------------------------------------')


 #visual_tree.render(file, view=True, format='png', cleanup=True, directory='./visual/', quiet=True)



# for i in range(len(files)):
#     print('Prueba ', i+1)
#     main(files[i])
#     # make the program wait for some seconds
#     time.sleep(3)

main(files[2])