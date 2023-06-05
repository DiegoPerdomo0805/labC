def scan_tokens(filename, ts):
    ignore = []
    productions = {}
    tokens = []

    variablesYalex = []
    for value in ts.values():
        temp = value.replace("return", "").replace(" ", "").strip()
        #print(temp)
        variablesYalex.append(temp)

    with open(filename, 'r') as f:
        content = f.read()

    #print(content)

    is_parsing_tokens = False
    token = ''
    production = ''
    inComment = False
    comentario = ''

    for symbol in content:
        #print(' - ', production)
        #print(' / ', symbol)
        if production == '/*':
            inComment = True
            production = ''
            continue

        # Comment
        if inComment:
            comentario += symbol

            if comentario.__contains__('*/'):
                inComment = False
                comentario = ''
            continue

        # Ignore
        if "IGNORE" in production:
            token = production
            production = ''
            is_parsing_tokens = True

        # Parsing tokens
        if is_parsing_tokens:
            #print(' * Earthbreaker Groon')
            if symbol == '%':
                is_parsing_tokens = False
            elif symbol == '\n':
                if 'token' in token:
                    token = token.split(' ', 1)[1]

                    if " " in token:
                        for t in token.split(" "):
                            t = t.strip()

                            if t.strip() in variablesYalex:
                                tokens.append(t)
                            else:
                                raise Exception('Token not defined in Yalex:', t)
                    else:
                        if token.strip() in variablesYalex:
                            tokens.append(token.strip())
                        else:
                            raise Exception('Token not defined in Yalex:', token)

                    token = ''
                    is_parsing_tokens = False
                elif 'IGNORE' in token:
                    token = token.replace("IGNORE", "").strip()
                    ignore.append(token)
                    token = ''
                    is_parsing_tokens = False
                else:
                    raise Exception('Error in token declaration:', token)
            else:
                token += symbol

        # Parsing productions
        else:
            if symbol == ";":
                production = production.split(':')
                lhs = production[0].strip()
                rhs = [p.strip() for p in production[1].split("|")]

                productions[lhs] = rhs if len(rhs) > 1 else [rhs[0]]
                production = ''
            else:
                if symbol == '%':
                    #print(' * Craven Edge')
                    is_parsing_tokens = True
                elif symbol == '\n' or symbol == '\t':
                    pass
                else:
                    production += symbol

    return tokens, productions

from AFN_to_AFD import state as STATE


def replaceToken(cadena, tokens):
    for token in tokens:
        if token.lower() in cadena:
            cadena = cadena.replace(token.lower(), token)
    return cadena


def startingPoint(productions):
    initial = ''
    for e in productions:
        for e2 in productions[e]:
            for e3 in productions.keys():
                if e3 in e2:
                    pass
                else:
                    initial = e

    new_initial = initial
    return new_initial
        
def create_state(productions, initial):
    # Create initial state
    content = {}
    for production in productions[initial]:
        #content.append(initial + " => " + production)
        content[initial] = [production]
    #print(content)
    initial_state = STATE(initial, content)
    initial_state.isInitial = False

    # Apply closure operation
    initial_state.contains = closure(initial_state, productions)

    return initial_state




def closure(state, productions):
    state_contains = state.contains
    items_to_add = []
    #print(' / contenido ', state_contains)
    # select all productions that coincide with the symbol after the dot
    # in the state contains
    for item in list(state_contains.keys()):
        for exp in state_contains[item]:
            dot_index = exp.index('.')
            if dot_index < len(exp) - 1:
                #symbol_after_dot = exp[dot_index + 1:]
                space_index = -1 
                for i in range(dot_index + 1, len(exp)):
                    if exp[i] == ' ':
                        space_index = i
                        break
                    elif i == len(exp) - 1:
                        space_index = len(exp)
                        break
                symbol_after_dot = exp[dot_index + 1:space_index+1]
                symbol_after_dot = symbol_after_dot.strip()
                #print(' / symbol ', symbol_after_dot)
                #if symbol_after_dot == 'expression':
                #    print(' / Jaghatai Khan')
#
                if symbol_after_dot in productions:
                    for production in productions[symbol_after_dot]:
                        #print('  / produccion ', production)
                        production = '.' + production
                        if symbol_after_dot not in state_contains:
                            items_to_add.append((symbol_after_dot, production))
                        else:
                            if production not in state_contains[symbol_after_dot]:
                                items_to_add.append((symbol_after_dot, production))
    #print(' / items ', items_to_add)
    if len(items_to_add) > 0:
        for item in items_to_add:
            #print(' / ', item)
            if item[0] not in state_contains:
                state_contains[item[0]] = []
            state_contains[item[0]].append(item[1])
        items_to_add.clear()
    return state_contains


def obtainTransitionS(state):
    content = state.contains
    transitions = []
    for e in content:
        for trans in content[e]:
            if '.' in trans:
                index = trans.index('.')
                if index < len(trans) - 1:
                    til = 0
                    for i in range( index + 1, len(trans)):
                        if i == len(trans) -1:
                            til = i
                            break
                        elif trans[i] == ' ' and i != index + 1:
                            til = i - 1
                            break
                        elif trans[i] == ' ' and i == index + 1:
                            til = til + 1
                            break
                    index = index + 1
                    til = til + 1
                    tran_temp = trans[index:til]
                    #print(' / ', tran_temp)
                    if tran_temp not in transitions:
                        transitions.append(tran_temp)
    return transitions


@DeprecationWarning
def goto(state, transition, productions):
    new_state = STATE(transition, {})
    for e in state.contains:
        if '.' in state.contains[e]:
            #print(' * Jaghatai Khan')
            index = state.contains[e].index('.')
            if index < len(state.contains[e]) - 1:
                til = 0
                for i in range(index + 1, len(state.contains[e])):
                    if i == len(state.contains[e]) - 1:
                        til = i
                        break
                    elif state.contains[e][i] == ' ' and i != index + 1:
                        til = i - 1
                        break
                    elif state.contains[e][i] == ' ' and i == index + 1:
                        til = til + 1
                        break
                index = index + 1
                til = til + 1
                tran_temp = state.contains[e][index:til]
                #print('   /   ',tran_temp)
                if tran_temp == transition:
                    new_state.contains[e] = state.contains[e].replace('.' + transition, transition + '.')
                    # check if the next symbol is a blank space
                    if til < len(state.contains[e]) - 1:
                        if new_state.contains[e][til] == ' ':
                            # swap the blank space with the dot
                            temp = new_state.contains[e][:til-1] + '.' + new_state.contains[e][til + 1:]
                            new_state.contains[e] = temp
                    # Keep record of the transitions in the state
                    if transition not in new_state.transitions:
                        new_state.transitions[transition] = new_state


    new_state.contains = closure(new_state, productions)
    return new_state


# Este método toma en consideración que el contenido de los estados son
# diccionarios, donde la llave es el símbolo no terminal y el valor es
# una lista de producciones 
def GoTo(state, transition, productions):
    #print(' /// transition: ', transition)
    is_there_transition = False
    new_state = STATE(transition, {})
    for e in state.contains:
        for exp in state.contains[e]:
            #print(' / exp: ', exp)
            dot_index = exp.index('.')
            if dot_index < len(exp) - 1:
                #symbol_after_dot = exp[dot_index + 1:]
                space_index = -1 
                for i in range(dot_index + 1, len(exp)):
                    if exp[i] == ' ':
                        space_index = i
                        break
                    elif i == len(exp) - 1:
                        space_index = len(exp)
                        break
                symbol_after_dot = exp[dot_index + 1:space_index+1]
                symbol_after_dot = symbol_after_dot.strip()
                transition = transition.strip()
                #print(' / symbol: ', symbol_after_dot, type(symbol_after_dot))
                #print(' / transition: ', transition, type(transition))
                #print(' / symbol ', symbol_after_dot)
                #print(' / comparacion: ', symbol_after_dot == transition)
                if symbol_after_dot == transition:
                    # transición del estado actual al nuevo estado
                    is_there_transition = True
                    #state.addTransition(transition, new_state)
                    production = exp.replace('.' + transition, transition + '.')
                    production = movePoint(production)
                    #print(' / produccion: ', production)
                    if e not in new_state.contains:
                        new_state.contains[e] = []
                    new_state.contains[e].append(production)
            #print(' * ' * 25)
    new_state.contains = closure(new_state, productions)
    if is_there_transition:
        state.addTransition(transition, new_state)
    return new_state
    

import time


@DeprecationWarning
def createAFD(productions, initial):
    states = []
    states_to_process = []
    processed_states = []
    states.append(initial)
    states_to_process.append(initial)

    while len(states_to_process) > 0:
        #print(' * Jaghatai Khan')
        state = states_to_process.pop(0)
        """print(' * ', state)
        print(' * ', state.contains)
        print(' * ', state.transitions)"""

        processed_states.append(state)

        for transition in obtainTransitionS(state):
            new_state = goto(state, transition, productions)
            if new_state not in states:
                states.append(new_state)
                states_to_process.append(new_state)
        time.sleep(3)

    return states


def movePoint(exp):
    # si el punto está al final de la expresión, no se puede mover
    # si el punto está antes de un espacio, este se puede mover
    index = exp.index('.')
    if index < len(exp) - 1: # si el punto no está al final de la expresión
        if exp[index + 1] == ' ':
            temp = exp[:index] + ' ' + '.' + exp[index + 2:]
            return temp
        else:
            return exp
    else:
        return exp
    

def alreadyExists(state, states):
    for s in states:
        if s.contains == state.contains:
            return True
    return False


def createAFD2(productions, initial):
    states = []
    states_to_process = []
    processed_states = []
    states.append(initial)
    states_to_process.append(initial)

    while len(states_to_process) > 0:
        state = states_to_process.pop(0)
        processed_states.append(state)

        for transition in obtainTransitionS(state):
            new_state = GoTo(state, transition, productions)
            if not alreadyExists(new_state, states):
                states.append(new_state)
                states_to_process.append(new_state)
            else:
                for s in states:
                    if s.contains == new_state.contains:
                        state.addTransition(transition, s)
                        break

    for s in states:
        s.isAccept = isAcceptanceState(s)
    return states


def isAcceptanceState(state):
    for e in state.contains:
        for exp in state.contains[e]:
            if exp[-1] == '.':
                return True
    return False

import graphviz

def createGraph(states):
    dot = graphviz.Digraph(comment='AFD')
    for s in states:
        if s.isAccept:
            dot.node(s.name, s.name, shape='doublecircle')
        else:
            dot.node(s.name, s.name)
        for t in s.transitions:
            dot.edge(s.name, s.transitions[t].name, t)
    dot.render('./visual_results/AFD_Grammar.gv', view=True)
