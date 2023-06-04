# primera parte de la minimización es dividir los estados en aceptación y no aceptación

# la segunda parte, y técnicamente recursiva, es continuar dividiendo los estados en grupos máds pequeños hasta que no se pueda más
from AFN_to_AFD import state
import graphviz
from AFN import *


def getTransitions(group, groups , sigma):
    transitions = {}
    for e in group:
        transitions[e.name] = {}
        for s in sigma:
            if e.checkTransition(s) != None:
                indice = -1
                for f in groups:
                    if e.checkTransition(s) in f:
                        indice = groups.index(f)
                #transitions.append([e.name, s,  indice])
                #transitions[e.name, s] = indice
                transitions[e.name][s] = indice
            else:
                #transitions.append([e.name, s,  None])
                #transitions[e.name, s] = None
                transitions[e.name][s] = None
    return transitions


#print(' - ',getTransitions(groups[0], groups, sigma))


# subdivide los grupos en subgrupos si es que no son atómicos

def isAtomic(grupo, grupos, sigma):
    if len(grupo) == 1:
        return True
    else:
        #transitions = []
        transitions = getTransitions(grupo, grupos, sigma)
        #print(transitions)

        first = transitions[grupo[0].name]

        flag = True
        #print(first)
        for i in range(1, len(grupo)):
            temp = transitions[grupo[i].name]
            #print(temp)
            #print(temp == first)
            if temp  != first:  
                flag = False
        
        return flag

        
    
def Divide(group, grupos, sigma):
    subgroups = [group]
    #print('subgroups', subgroups)
    i = 0
    while i < len(subgroups):
        subgroup = subgroups[i]
        if not isAtomic(subgroup, grupos, sigma):
            transitions = getTransitions(subgroup, grupos, sigma)
            #for e in transitions:
            #    print( ' - ', e, transitions[e])
            for target_group in transitions.values():
                new_subgroup = [s for s in subgroup if transitions[s.name] == target_group]
                if new_subgroup not in subgroups:
                    subgroups.append(new_subgroup)
            subgroups.remove(subgroup)
            i -= 1
        i += 1
    for e in subgroups:
        if not isAtomic(e, grupos, sigma):
            #print('entré 159')
            Divide(e, grupos, sigma)
    #return subgroups
    #print('subgroups')
    grupos.remove(group)
    grupos.extend(subgroups)
    #print('grupos')
    #for e in grupos:
    #    temp = []
    #    for f in e:
    #        temp.append(f.name)
    #        #print(f.name, end=' ')
    #    #print('\n')
    #    print(temp)



def allAtomic(grupos, sigma):
    flag = True
    for e in grupos:
        if not isAtomic(e, grupos, sigma):
            flag = False
    return flag


def Minimization(AFD, sigma):
    groups = []
    accept = []
    not_accept = []
    for e in AFD:
        if e.isAccept:
            accept.append(e)
        else:
            not_accept.append(e)

    groups.append(accept)
    if not_accept != []:
        groups.append(not_accept)

    #print('grupos iniciales')
    #for e in groups:
    #    temp = []
    #    for f in e:
    #        temp.append(f.name)
    #        #print(f.name, end=' ')
    #    #print('\n')
    #    print(temp)
    flag = True
    while flag:
        for e in list(groups):
            #print(isAtomic(e, groups, sigma),'\n')
            if isAtomic(e, groups, sigma):
                #print(e, 'es atómico')
                flag = not allAtomic(groups, sigma)
            else:
                #print(e, 'no es atómico')
                Divide(e, groups, sigma)
                flag = not allAtomic(groups, sigma)
                #print(groups)
                #print('\n')
    
    #print(groups)
    
    # crear estados usando state class
    inicial = AFD[0]
    #print('  ** inicial', inicial.name, inicial)
    
    
    new_states = []
    i = 0
    for e in groups:
        #print( '  **  ' , e)
        new_s = state( f"q{i}", e)
        if inicial in e:
            new_s.isInitial = True
        new_states.append(new_s)
        i += 1
    
    for e in new_states:
        #print(e.name)
        for s in sigma:
            transition = None
            if e.contains[0].checkTransition(s) != None:
                transition = e.contains[0].transitions[s]
            if transition != None:
                for e2 in new_states:
                    if transition in e2.contains:
                        e.addTransition(s, e2)
    
            else:
                e.addTransition(s, None)

    # aceptación
    for e in new_states:
        for e2 in e.contains:
            if e2.isAccept:
                e.isAccept = True
                break

    return new_states


def Minimizacion_Visual(AFD, metodo, exp):
    g = graphviz.Digraph(comment='AFD_from_AFN', format='png')
    g.attr('node', shape='circle')
    g.attr('node', style='filled')
    g.attr('node', color='lightblue2')
    g.attr('node', fontcolor='black')
    g.attr('edge', color='black')
    g.attr('edge', fontcolor='black')
    g.attr('edge', fontsize='20')
    g.attr('graph', rankdir='LR')
    g.attr('graph', size='17')
    g.attr(label=exp)


    for e in AFD:
        if e.isAccept:
            g.node(e.name, e.name, shape='doublecircle')
        else:
            g.node(e.name, e.name)
        for k, v in e.transitions.items():
            if v != None:
                g.edge(e.name, v.name, label=k)
    g.render(metodo, view=True, directory='./visual_results/') 




