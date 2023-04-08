
operators = ["+", "*", "?", "|", "(", ")", ".", "[", "]"]

# validar la existencia de reglas repetidas
def repeated_rule(r, l):
    # Check for invalid rule names
    for key in r:
        if len(key) > 1 and key not in l:
            # Ignore rule names with quotes
            if key.count("'") == 2 or key.count('"') == 2:
                continue
            raise Exception("Invalid rule name: " + key)


# generar la gramatica a partir del archivo .yal
def grammar(file):
    with open(file, 'r') as f:
        yal = f.read().splitlines()
        let_rules = []

        for l in yal:
            nl = l.strip()

            if nl != '' and nl[0] != '#':
                #print(nl)
                if '(*' in nl:
                    #print(nl.index('(*'))
                    nl = nl[:nl.index('(*')]
                    nl = nl.strip()
                    #print(' - ', nl)
                    if nl != '':
                        let_rules.append(nl)
                else:
                    let_rules.append(nl)
        lets = []
        rules = []
        rulesFlag = False

        for e in let_rules: 
            if rulesFlag:
                rules.append(e)
            else:
                if e.startswith('rule'):
                    rulesFlag = True
                    #print('rules')
                else:
                    lets.append(e)

        l = {} # let
        r = {} # rules

        # diccionario de reglas de formato let
        for let in lets:

            # separar la sentencia let en dos partes, la variable y el valor
            let = let.replace("let ", "")
            let = let.strip()
            let = let.split("=")

            letVal = let[1].strip()

            # valor de la sentencia let en forma de arreglo
            if letVal.startswith("[") and letVal.endswith("]"):
                # si el valor arreglo tiene un rango
                if "-" in letVal:
                    letVal = letVal[1:-1]
                    #print(' - ', let ,' let interval value: ',letVal)

                    tempArray = []
                    lastIndex = 0
                    count = letVal.count("-")

                    for x in range(count):
                        index = letVal.index("-", lastIndex)

                        startA = letVal.index("'", lastIndex)
                        endA = letVal.index("'", startA + 1)

                        startB = letVal.index("'", index)
                        endB = letVal.index("'", startB + 1)

                        valA = letVal[startA + 1:endA]
                        valB = letVal[startB + 1:endB]

                        tempArray.append(valA + "-" + valB)

                        lastIndex = endB + 1

                # si el valor arreglo no tiene un rango, sino que
                # es un arreglo de caracteres especificos
                else:

                    #print(' - ', let ,' let array value: ',letVal)

                    testCount = letVal.count("'")
                    if testCount == 0:
                        testCount = letVal.count('"')

                    if testCount > 2:
                        letVal = letVal[1:-1]

                        tempArray = []
                        currentIndex = -1
                        for x in range(len(letVal)):
                            char = letVal[x]

                            if currentIndex > x:
                                continue
                            elif currentIndex == x:
                                currentIndex = -1

                            if char == "'":
                                if currentIndex == -1:
                                    currentIndex = x

                            elif currentIndex != -1:
                                start = currentIndex + 1
                                end = letVal.index("'", start)

                                tempArray.append(letVal[start:end])
                                currentIndex = end + 1

                    else:
                        letVal = letVal[1:-1]

                        if "\\" in letVal:
                            letVal = letVal[1:-1]

                            tempArray = []
                            for char in letVal:
                                if char != "\\":
                                    tempArray.append("\\" + char)

                        else:
                            tempArray = []
                            for char in letVal:
                                if char != "'" and char != '"':
                                    tempArray.append(char)

                letVal = tempArray

            l[let[0].strip()] = letVal

        # diccionario de reglas de formato rule
        for rule in rules:
            #print(' - ', rule ,' rule value: ')
            rule = rule.replace("rule ", "")
            if "return" in rule:
                start = rule.index("{")
                end = rule.index("}")
                returnVal = rule[start + 1:end].strip() + rule[end + 1:].strip()

                if "'" in rule:
                    start = rule.index("'")
                    end = rule.index("'", start + 1)
                    ruleName = rule[start + 1:end].strip()
                else:
                    start = 0
                    if "|" in rule:
                        start = rule.index("|") + 1

                    end = rule.index("{")
                    ruleName = rule[start:end].strip()
                r[ruleName] = returnVal
            else:
                r[rule.strip()] = ""

        repeated_rule(r, l)

        return l, r


# generar el alfabeto a partir de las reglas let y rule
# además de generar el regex a partir de las reglas rule
def generate_alphabet(l, r):
    alphabet = []
    operators = ["[", "]", "|", "'", "\""]
    regex = []

    for key in l:
        if isinstance(l[key], list):
            newVals = []
            case = 0

            for val in l[key]:
                if isinstance(val, str) and "-" in val:
                    case = 1
                    break
                elif isinstance(val, str) and "\\" in val:
                    case = 2
                    break

            if case == 1:
                for val in l[key]:
                    start = ord(val[0])
                    end = ord(val[2])

                    for x in range(start, end + 1):
                        alphabet.append(chr(x))
                        newVals.append(chr(x))

                l[key] = newVals

            elif case == 2:
                newVals = []
                for val in l[key]:
                    if val.startswith("\\"):
                        val = val.replace("\\", "")

                        if val == "n":
                            newVals.append(ord("\n"))
                        elif val == "t":
                            newVals.append(ord("\t"))
                        elif val == "r":
                            newVals.append(ord("\r"))
                        elif val == "f":
                            newVals.append(ord("\f"))
                        elif val == "s":
                            newVals.append(ord(" "))
                        else:
                            raise Exception("Invalid escape character: " + val)
                    else:
                        newVals.append(ord(val))

                for val in newVals:
                    alphabet.append(val)

                l[key] = newVals

            else:
                for val in l[key]:
                    alphabet.append(val)

    for key in r:
        if key in l:
            val = l[key]
            x = 0

            while True:
                if val[x] in operators:
                    if val[x] == "[":
                        x += 1
                        regex.append("(")

                        while not val[x] == "]":
                            if val[x] != "'":
                                if val[x] in operators or val[x] == "-":
                                    regex.append("'" + str(ord(val[x])) + "'")
                                    alphabet.append(ord(val[x]))
                                else:
                                    regex.append(val[x])
                                    alphabet.append(val[x])

                                regex.append("|")

                            x += 1

                        regex.pop()
                        regex.append(")")

                        x += 1

                    else:
                        x += 1

                else:
                    tempStr = ""
                    while not val[x] in operators:
                        tempStr += val[x]
                        x += 1

                        if x >= len(val):
                            break

                    if tempStr in l and isinstance(l[tempStr], str):
                        tempOperators = ""
                        newTempStr = ""

                        for char in l[tempStr]:
                            if char in operators:
                                tempOperators += char
                            else:
                                newTempStr += char

                        if newTempStr in l:
                            regex.append(newTempStr)

                            for char in tempOperators:
                                regex.append(char)
                                regex.append("|")

                            regex.pop()

                        else:
                            regex.append(tempStr)

                    else:
                        if "'" in tempStr:
                            tempStr = tempStr.replace("'", "")

                        if len(tempStr) > 0:
                            if len(tempStr) == 1:
                                alphabet.append(tempStr)

                            regex.append(tempStr)

                    if x >= len(val):
                        break

            if key != list(r.keys())[-1]:
                regex.append("|")

        else:
            for char in key:
                regex.append("'" + str(ord(char)) + "'")
                alphabet.append(ord(char))
                regex.append("|")

            regex.pop() # Remove last "|"
            if key != list(r.keys())[-1]:
                regex.append("|")


    return alphabet, regex


# traducir el regex a partir de las reglas ya definidas
def parser(regexStack, lets, sigma):
    regex = ""
    regex2 = []
    
    for val in regexStack:
        if val in lets:
            regex += "("
            regex2.append("(")

            for x in range(len(lets[val])):
                if (len(regex) > 0 and 
                    regex[-1] != "(" and 
                    regex[-1] != ")" and 
                    lets[val][x] != "(" and
                    lets[val][x] != ")"):

                    regex = regex + "|"
                    regex2.append("|")

                if isinstance(lets[val][x], int):
                    regex += "'" + str(lets[val][x]) + "'"
                    regex2.append(lets[val][x])
                else:
                    regex += lets[val][x]
                    regex2.append(lets[val][x])


                    if (lets[val][x] not in sigma and
                        lets[val][x] != "(" and
                        lets[val][x] != ")" and
                        lets[val][x] not in operators):

                        sigma.append(lets[val][x])

            regex += ")"
            regex2.append(")")
            
        else:
            regex += val
            val = val.strip("'")
            regex2.append(val)
    
    return regex2, sigma
