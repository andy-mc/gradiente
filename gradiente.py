import re
import numpy as np
from sympy import Symbol, Derivative
from math import sqrt


def hessian_matrix(derivatives):
    matrix = []
    for d in derivatives:
        row = re.findall("(-?\d[\\.\d]*)\\*", str(d).replace(" ", ""))
        matrix.append([float(num) for num in row])
    return np.array(matrix)


def numpy_fillna(data):
    # Get lengths of each row of data
    lens = np.array([len(i) for i in data])
    # Mask of valid places in each row
    mask = np.arange(lens.max()) < lens[:,None]
    # Setup output array and put elements from data into masked positions
    out = np.zeros(mask.shape, dtype=data.dtype)
    out[mask] = np.concatenate(data)
    return out    


def make_derivatives(derivatives):
    return np.array([[eval(str(d))] for d in derivatives])


function = raw_input("\nEscribe tu funcion: ")

matched_variable = re.findall(r"x\d", function)
variables = sorted(list(set(matched_variable)))

derivatives = []
for var in variables:
    x = Symbol(var)
    partialderiv= Derivative(function, x)
    derivatives.append(partialderiv.doit())
    exec('{} = 0.1'.format(var))


f2 = 1
alfa = 0
gradient = None
S = [[0] for d in derivatives]

counter = 0
while not (sqrt(f2) <= 0.0001):
    counter += 1
    for i in range(len(variables)):
        exec("x{} += alfa * S[{}][0]".format(i+1, i))

    gradient = numpy_fillna(make_derivatives(derivatives))
    hmatrix = numpy_fillna(hessian_matrix(derivatives))
    f2 = sum([g**2 for g in gradient])
    try:
        denom_alfa = np.sum(gradient * (hmatrix * np.transpose(gradient)))
    except ValueError as error:
        print error
        print "No es posible multiplicar la matriz hessiana y la matriz gradiente"
        break

    if str(denom_alfa) == 'nan' or denom_alfa == 0:
        print 'denominador alfa es nan o 0'
        break

    alfa = sum(f2/denom_alfa)
    S = gradient * -1

print '\nValores de las variables:'
for var in variables:
    print "%s: " % var, eval(var)

print "\nNumero de iteraciones:", counter
print    
print 'Valor optimo:', eval(function), "\n"

raw_input("")

