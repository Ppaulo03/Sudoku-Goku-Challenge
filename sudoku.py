from copy import deepcopy
import pdb


def show_matriz(matriz):

    print()
    cont_row = 2
    for line in matriz:
        cont_line = 2
        for num in line:
            print(num, end=" ")
            if not cont_line:
                cont_line = 2
                print(end="   ")
            else:
                cont_line -= 1
        print("")
        if not cont_row:
            cont_row = 2
            print()
        else:
            cont_row -= 1


def transformar_em_listas(matriz):

    new_matriz = [
        [[col] if type(col) is not list else col for col in lin]
        for lin in matriz]

    return new_matriz


def transformar_em_numero(matriz):

    new_matriz = [
        [int(str(col)[1:-1]) if type(col) is list else col for col in lin]
        for lin in matriz]

    return new_matriz


def transposta(matriz):
    try:

        transposta = [
            [linha[col] for linha in matriz]
            for col in range(len(matriz[0]))
        ]
        return transposta

    except IndexError:
        raise IndexError("Lista fornecida não caracteriza uma matriz")


def separar_quadrantes(matriz):

    separado = list()
    size = int(len(matriz)/3)
    for line_quad in range(size):
        for row_quad in range(size):

            quadrante = [
                [
                    matriz[line+(line_quad*3)][row+(row_quad*3)]
                    for row in range(size)
                ]for line in range(size)]

            separado.append(quadrante)
    return separado


def juntar_quadrantes(matriz):
    fusao = list()
    new_lin = list()
    for lin_quad in range(0, 9, 3):
        for linha in range(3):
            for col_quad in range(3):
                new_lin.extend(matriz[col_quad+lin_quad][linha])
            fusao.append(new_lin)
            new_lin = []
    return fusao


def determinar_possibilidades(sudoku, pos_lin, pos_col):

    if 0 in sudoku[pos_lin][pos_col]:
        possibilidades = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    elif len(sudoku[pos_lin][pos_col]) == 1:
        return sudoku[pos_lin][pos_col]
    else:
        possibilidades = set(sudoku[pos_lin][pos_col])

    linhas = sudoku
    colunas = transposta(sudoku)
    quadrantes = separar_quadrantes(sudoku)
    pos_quad = int(pos_col/3) + (int(pos_lin/3)*3)

    pos_ocpd = {item[0] for item in linhas[pos_lin] if len(item) == 1}
    possibilidades = possibilidades.difference(pos_ocpd)

    pos_ocpd = {item[0] for item in colunas[pos_col] if len(item) == 1}
    possibilidades = possibilidades.difference(pos_ocpd)

    for lin in quadrantes[pos_quad]:
        for item in lin:
            if len(item) == 1:
                pos_ocpd.add(item[0])
    possibilidades = possibilidades.difference(pos_ocpd)

    return list(possibilidades)


def marcar_possibilidades(sudoku):
    finished = False
    old_matriz = sudoku

    while not finished:
        finished = True
        new_matriz = list()
        new_line = list()
        for idx_lin, linha in enumerate(old_matriz):
            for idx_col, item in enumerate(linha):

                solucoes = determinar_possibilidades(
                    old_matriz, idx_lin, idx_col)

                if solucoes != item:
                    finished = False
                new_line.append(solucoes)

            new_matriz.append(new_line)
            new_line = []
        old_matriz = new_matriz[:]
    return new_matriz


def pegar_duplicata(matriz, lin, dupla):
    linha = matriz[lin]
    for item in linha:
        if item is not dupla and item == dupla:
            for x in range(len(linha)):
                if linha[x] is not dupla and linha[x] is not item:
                    for num in dupla:
                        if num in linha[x]:
                            matriz[lin][x].remove(num)
            break
    return matriz


def eliminar_duplicata(sudoku, pos_lin, pos_col):

    if len(sudoku[pos_lin][pos_col]) != 2:
        return sudoku

    quad = separar_quadrantes(sudoku)
    quad_lin = (int(pos_lin/3)*3)
    quad_col = int(pos_col/3)
    pos_quad = quad_lin + quad_col

    sudoku = pegar_duplicata(sudoku, pos_lin, sudoku[pos_lin][pos_col])

    sudoku = transposta(sudoku)
    sudoku = pegar_duplicata(sudoku, pos_col, sudoku[pos_col][pos_lin])
    sudoku = transposta(sudoku)

    target = sudoku[pos_lin][pos_col]
    pos = quad[pos_quad]
    for quad_l in pos:
        for quad_it in quad_l:
            if quad_it is not target and quad_it == target:

                for id_line, line in enumerate(pos):
                    for row, item in enumerate(line):
                        if item is not target and item is not quad_it:
                            for num in target:
                                if num in item:
                                    quad[pos_quad][id_line][row].remove(num)

                break

    sudoku = juntar_quadrantes(quad)
    return sudoku


def checar_duplicatas(sudoku):
    new_matriz = sudoku

    for idx_lin, linha in enumerate(new_matriz):
        for idx_col in range(len(linha)):
            new_matriz = eliminar_duplicata(new_matriz, idx_lin, idx_col)
    return new_matriz


def check_routine(sudoku):

    if sudoku == []:
        return sudoku

    new_matriz = sudoku
    old_matriz = []

    while old_matriz != new_matriz:

        old_matriz = new_matriz
        new_matriz = marcar_possibilidades(new_matriz)
        new_matriz = checar_duplicatas(new_matriz)
        new_matriz = marcar_possibilidades(new_matriz)

    for linhas in new_matriz:
        for item in linhas:
            if item == []:
                return []

    return new_matriz


def tentativa_erro(sudoku):

    sudoku = check_routine(sudoku)
    if sudoku == []:
        return []

    new_matriz = []
    for idx_lin in range(len(sudoku)):
        for idx_col in range(len(sudoku[idx_lin])):

            if len(sudoku[idx_lin][idx_col]) == 2:
                new_matriz = deepcopy(sudoku)
                sudoku[idx_lin][idx_col].remove(sudoku[idx_lin][idx_col][0])
                sudoku = tentativa_erro(sudoku)

                if sudoku == []:

                    sudoku = deepcopy(new_matriz)

                    sudoku[idx_lin][idx_col].remove(
                        sudoku[idx_lin][idx_col][1])

                    sudoku = tentativa_erro(sudoku)

                    if sudoku == []:
                        return []

    return sudoku


# example = [
#     [0, 0, 0,  0, 0, 0,  0, 0, 0],
#     [0, 0, 0,  0, 0, 0,  0, 0, 0],
#     [0, 0, 0,  0, 0, 0,  0, 0, 0],

#     [0, 0, 0,  0, 0, 0,  0, 0, 0],
#     [0, 0, 0,  0, 0, 0,  0, 0, 0],
#     [0, 0, 0,  0, 0, 0,  0, 0, 0],

#     [0, 0, 0,  0, 0, 0,  0, 0, 0],
#     [0, 0, 0,  0, 0, 0,  0, 0, 0],
#     [0, 0, 0,  0, 0, 0,  0, 0, 0]
# ]


example = [
    [5, 0, 0,  0, 0, 0,  2, 3, 0],
    [0, 0, 0,  0, 4, 8,  9, 7, 0],
    [0, 8, 0,  0, 0, 3,  0, 0, 0],

    [1, 0, 0,  3, 0, 9,  7, 4, 0],
    [0, 0, 0,  0, 0, 6,  0, 0, 0],
    [8, 9, 0,  0, 0, 0,  0, 0, 0],

    [0, 4, 0,  0, 0, 0,  0, 6, 0],
    [6, 2, 0,  8, 3, 0,  0, 0, 1],
    [0, 5, 1,  0, 6, 0,  0, 2, 0]
]

# [5] [1] [4]    [6] [9] [7]    [2] [3] [8]
# [2] [3] [6]    [1] [4] [8]    [9] [7] [5]
# [7] [8] [9]    [5] [2] [3]    [6] [1] [4]

# [1] [6] [5]    [3] [8] [9]    [7] [4] [2]
# [4] [7] [3]    [2] [5] [6]    [1] [8] [9]
# [8] [9] [2]    [4] [7] [1]    [3] [5] [6]

# [3] [4] [8]    [9] [1] [2]    [5] [6] [7]
# [6] [2] [7]    [8] [3] [5]    [4] [9] [1]
# [9] [5] [1]    [7] [6] [4]    [8] [2] [3]


example = transformar_em_listas(example)
example = tentativa_erro(example)
# example = transformar_em_numero(example)
show_matriz(example)
