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
    content = []
    for production in productions[initial]:
        content.append(initial + " => " + production)
    initial_state = STATE(initial, content)
    initial_state.isInitial = True

    # Apply closure operation
    state_contains = initial_state.contains
    while True:
        new_items_added = False
        for item in state_contains:
            #print(item)
            dot_index = item.index('.')
            # . indicates where the parser is currently at
            if dot_index < len(item) - 1:
                symbol_after_dot = item[dot_index + 1:]
                #print(symbol_after_dot)

                if symbol_after_dot in productions:

                    for production in productions[symbol_after_dot]:
                        new_item = symbol_after_dot + ' => .' + production
                        
                        if new_item not in state_contains:
                            state_contains.append(new_item)
                            new_items_added = True

        if not new_items_added:
            break

    return initial_state



