#file = './tests/slr-1.yal'

from yalex import grammar, generate_alphabet, parser

files = [
    './tests/slr-1.yal',
    './tests/slr-2.yal',
    './tests/slr-3.yal',
    './tests/slr-4.yal'
]

file = files[3]



print('-------------------------------------------------------------')    

l, r = grammar(file)
sigma, regex = generate_alphabet(l, r)



for e in l:
    print(e, ' = ', l[e])

print('\n')
print('Cassandra de Rolo')
print('-------------------------------------------------------------')

for e in r:
    print(e, ' = ', r[e])

print('\nPercival Frederickstein von Musel Klossowski de Rolo III')
print('-------------------------------------------------------------')


print('Alfabeto: ', sigma)
print('Expresion regular: ', regex)

print('\n-------------------------------------------------------------')


r, sigma = parser(regex, l, sigma)

print('Expresion regular: ', r)
print('Alfabeto: ', sigma)

print('Keyleth')
print('-------------------------------------------------------------')

