from _operator import or_

import  numpy as np
import itertools
import random

from random import randrange


# orden_numerico = np.arange(0, 16)
# lista_permutaciones_posibles = itertools.permutations(orden_numerico, 2)
# lista_permutaciones_posibles = list(lista_permutaciones_posibles)
#
#
#
# lista_frecuencia = []
# for p in lista_permutaciones_posibles:
#     lista_frecuencia.append([p,0])
#
# # print(lista_frecuencia[0][0])
# #
# valor1 = lista_frecuencia[0][0]
# valor2 = lista_frecuencia[2][0]
#
# print(valor1 , " " , valor2)
#
# lista_tabu = []
#
# for i in range(5):
#     lista_tabu.append(lista_frecuencia[i])
#
# print(lista_tabu)
# lista_tabu[0][1] += 1
#
# tupla_buscada = (0,4)
#
# encontrado = False
# i = 0
# while not encontrado:
#     lista_tabu[]
#
#
#
# s_act = s_inicial
# s_mejor = s_act
# lista_tabu =[]
# mejor_vecino = s_inicial
#
# (i,pos(i))
#
#
# (i,j,ppos(i),pos(j))
#
# while criterio:
#
#     vecinos = generar_vecinos(s_act)
#     for v in vecinos:
#
#         if(  coste(v) < coste(s_mejor) ):
#             mejor_vecino = v
#             s_mejor = v
#         if movimiento de v pertenece a lista_tabu:
#             saltmos break salgo busco vecino siguiente
#         elseif(coste(v) < coste(mejor_vecino)):
    #             mejor_vecino = v
    #
#     s_act = mejor_vecino
#     lista_tabu = lista_tabu.append(movimiento de mejor_vecino)
#     modifica lista_tabu (Es circular se borra el que lleva mas tiempo dentro)
#
#     if coste(mejor_vecino) < coste(s_mejor):
#         s_mejor = mejor_vecino
#
#
# return s_mejor


# acciones = genfromtxt('datos/deltas_5m.csv', delimiter=',')

def generar_vecinos_con_offset(solucion_actual, limite_vecinos, granularidad):
    vecinos_generados = []
    movimientos_realizados = []
    orden_numerico = np.arange(0,solucion_actual.shape[0])
    lista_permutaciones_posibles = itertools.permutations(orden_numerico, 2)
    lista_permutaciones_posibles = list(lista_permutaciones_posibles)

    if limite_vecinos > 240:
        limite_vecinos = 240

    r = random.randint(0, 240 + limite_vecinos + 1)
    i = r % (240 - limite_vecinos + 1)
    tam = limite_vecinos + i
    for v in lista_permutaciones_posibles:
        indiceA = lista_permutaciones_posibles[i][0]
        indiceB = lista_permutaciones_posibles[i][1]
        aux = solucion_actual.copy()
        if aux[indiceA] > granularidad:
            valorA = aux[indiceA]
            valorB = aux[indiceB]
            aux[indiceA] -= granularidad
            aux[indiceB] += granularidad
            elem_lista = [(indiceA, valorA), (indiceB, valorB)]
            movimientos_realizados.append(elem_lista)
            vecinos_generados.append(aux)
            i += 1

        elif aux[indiceB] > granularidad:
            valorA = aux[indiceA]
            valorB = aux[indiceB]
            aux[indiceA] += granularidad
            aux[indiceB] -= granularidad
            elem_lista = [(indiceA, valorA), (indiceB, valorB)]
            movimientos_realizados.append(elem_lista)
            vecinos_generados.append(aux)
            i += 1

        # elem_lista = [(indiceA,valorA),(indiceB,valorB)]
        # movimientos_realizados.append(elem_lista)
        # vecinos_generados.append(aux)
        # i += 1
        if i == tam:
            break
    return vecinos_generados,movimientos_realizados


a = [32, 12,  9, 15, 13,  1,  9,  3, 11, 22, 13, 22,  4,  1, 24, 29,]

b = [32, 12,  9, 15, 15,  1,  9,  3, 11, 22, 13, 20,  4,  1, 24, 29,]

vec, mov = generar_vecinos_con_offset(np.array(b),40,1)

print(vec)

print(np.array([32, 12,  9, 15, 13,  1,  9,  3, 11, 22, 13, 22,  4,  1, 24, 29,]).sum())

print(np.array([32, 12,  9, 15, 15,  1,  9,  3, 11, 22, 13, 20,  4,  1, 24, 29,]).sum())