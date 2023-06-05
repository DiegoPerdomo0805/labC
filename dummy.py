def closure(items, productions):
    while True:
        new_items_added = False
        for item in items:
            dot_index = item.index('.')
            if dot_index < len(item) - 1:
                symbol_after_dot = item[dot_index + 1]
                if symbol_after_dot in productions:
                    for production in productions[symbol_after_dot]:
                        new_item = symbol_after_dot + ' -> .' + production
                        if new_item not in items:
                            items.append(new_item)
                            new_items_added = True
        if not new_items_added:
            break

def goto(items, symbol, productions):
    new_items = []
    for item in items:
        dot_index = item.index('.')
        if dot_index < len(item) - 1 and item[dot_index + 1] == symbol:
            new_item = item[:dot_index] + symbol + '.' + item[dot_index + 2:]
            new_items.append(new_item)
    closure(new_items, productions)
    return new_items

# Example usage
productions = {
    'S': ['E'],
    'E': ['E + T', 'T'],
    'T': ['T * F', 'F'],
    'F': ['( E )', 'id']
}

items = ['S -> .E']
print(items)  # ['S -> .E']
for e in productions:
    closure(items, productions)
    print(' - ',items)  # ['S -> .E', 'E -> .E + T', 'E -> .T', 'T -> .T * F', 'T -> .F', 'F -> .( E )', 'F -> .id']
    new_items = goto(items, e, productions)
    print(e, new_items)  # ['S -> E.', 'E -> E. + T', 'E -> .E + T', 'E -> .T', 'T -> .T * F', 'T -> .F', 'F -> .( E )', 'F -> .id']
    closure(new_items, productions)
    print(' - ',new_items)  # ['S -> E.', 'E -> E. + T', 'E -> .E + T', 'E -> .T', 'T -> .T * F', 'T -> .F', 'F -> .( E )', 'F -> .id']
    print()


"""closure(items, productions)
print(items)  # ['S -> .E', 'E -> .E + T', 'E -> .T', 'T -> .T * F', 'T -> .F', 'F -> .( E )', 'F -> .id']

new_items = goto(items, 'E', productions)
print(new_items)  # ['S -> E.', 'E -> E. + T', 'E -> .E + T', 'E -> .T', 'T -> .T * F', 'T -> .F', 'F -> .( E )', 'F -> .id']
closure(new_items, productions)
print(new_items)  # ['S -> E.', 'E -> E. + T', 'E -> .E + T', 'E -> .T', 'T -> .T * F', 'T -> .F', 'F -> .( E )', 'F -> .id']
"""