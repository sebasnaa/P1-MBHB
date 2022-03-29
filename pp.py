import math
from _operator import or_
from builtins import list

import  numpy as np
import itertools
import random

from random import randint
from random import randrange

from numpy import genfromtxt


def existe_movimiento_tabu(lista_tabu,movimiento_actual):
    for par in lista_tabu:
        if movimiento_actual[0] == par[0] or movimiento_actual[0] == par[1] or movimiento_actual[1] == par[0] or movimiento_actual[1] == par[1]:
            return True

    return False

def reducir_tiempo_lista_tabu(lista_tabu):

    for par in lista_tabu:
        par[2] -=1

    for par in lista_tabu:
        if par[2] == 0:
            lista_tabu.remove(par)


    return lista_tabu

def agregar_lista_tabu(lista_tabu,movimiento_actual,longitud_lista_tabu_limite,duracion,indice_agregacion):

    if len(lista_tabu) == longitud_lista_tabu_limite:
        aux = movimiento_actual.copy()
        aux.append(duracion)
        lista_tabu[indice_agregacion] = aux
        indice_agregacion += 1
        indice_agregacion = indice_agregacion % longitud_lista_tabu_limite
    else:
        aux = movimiento_actual.copy()
        aux.append(duracion)
        lista_tabu.append(aux)
        indice_agregacion += 1
        indice_agregacion = indice_agregacion % longitud_lista_tabu_limite


    return lista_tabu,indice_agregacion



# lista_tabu = []
# longitud_lista_tabu_limite = 2
# duracion = 3
# indice_agregacion = 0
#
# a1 = (0,2)
# a2 = (1,4)
#
# b1 = (5,1)
# b2 = (6,7)
#
# c1 = (3,8)
# c2 = (2,21)
#
# d1 = (7,0)
# d2 = (14,11)
#
# m = [a1,a2]
#
#
# print(lista_tabu)
# movimiento_actual = []
# movimiento_actual.append(a1)
# movimiento_actual.append(a2)
# lista_tabu,indice_agregacion = agregar_lista_tabu(lista_tabu,movimiento_actual,longitud_lista_tabu_limite,duracion,indice_agregacion)
#
# reducir_tiempo_lista_tabu(lista_tabu)
# reducir_tiempo_lista_tabu(lista_tabu)
# print(lista_tabu)
#
#
# movimiento_actual = []
# movimiento_actual.append(b1)
# movimiento_actual.append(b2)
# lista_tabu,indice_agregacion = agregar_lista_tabu(lista_tabu,movimiento_actual,longitud_lista_tabu_limite,duracion,indice_agregacion)
# print(lista_tabu)
#
# reducir_tiempo_lista_tabu(lista_tabu)
#
# print(lista_tabu)




#
# movimiento_actual = []
# movimiento_actual.append(c1)
# movimiento_actual.append(c2)
# lista_tabu,indice_agregacion = agregar_lista_tabu(lista_tabu,movimiento_actual,longitud_lista_tabu_limite,duracion,indice_agregacion)
# print(lista_tabu)



#
# movimiento_actual = []
# movimiento_actual.append(c1)
# movimiento_actual.append(c2)
# lista_tabu,indice_agregacion = agregar_lista_tabu(lista_tabu,movimiento_actual,longitud_lista_tabu_limite,duracion,indice_agregacion)
# print(lista_tabu)
#
# movimiento_actual = []
# movimiento_actual.append(d1)
# movimiento_actual.append(d2)
# lista_tabu,indice_agregacion = agregar_lista_tabu(lista_tabu,movimiento_actual,longitud_lista_tabu_limite,duracion,indice_agregacion)
# print(lista_tabu)



#
# dim_lista_tabu = 2
# lista_tabu = list()
#
# indice = 0
#
# a1 = (0,2)
# a2 = (1,4)
#
# b1 = (5,1)
# b2 = (6,7)
#
# c1 = (3,8)
# c2 = (2,21)
#
# elem = []
# elem.append(a1)
# elem.append(a2)
# elem.append(3)
# lista_tabu.append(elem)
# indice+=1
# indice = indice % dim_lista_tabu
#
# elem = []
# elem.append(b1)
# elem.append(b2)
# elem.append(3)
# lista_tabu.append(elem)
# indice+=1
# indice = indice % dim_lista_tabu
#
#
#
# # si  longitud == tamaño ya hago [indice]
# elem = []
# elem.append(c1)
# elem.append(c2)
# elem.append(3)
# lista_tabu[indice] = elem
# indice+=1
# indice = indice % dim_lista_tabu
#
# elem = []
# elem.append(a1)
# elem.append(a2)
# elem.append(3)
# lista_tabu[indice] = elem
# indice+=1
# indice = indice % dim_lista_tabu
#
#
# print(indice)
#
# print(lista_tabu)
# print()



# movimiento_s_v = (3,8)
# for v in lista_tabu:
#     if(movimiento_s_v == v[0] or movimiento_s_v == v[1]):
#         print("tabu")
#         break
#     print("sigues??")
#     print(v[0] , "  " , v[1])



def actualizar_tabla_frecuencias(lista_frecuencias,s_act):
    valor_limite = 39
    for i in range(0,16):
        valor = s_act[i]
        if valor > valor_limite:
            indice_insercion = 7
        else:
            indice_insercion = np.floor(valor / 5)

        lista_frecuencias[i][int(indice_insercion)] = lista_frecuencias[i][int(indice_insercion)] + 1
    return lista_frecuencias


def calcular_inversa(lista_valores):
    solucion = []
    for indice,valor in enumerate(lista_valores):
        if valor > 0:
            solucion.append(1/valor)
        else:
            solucion.append(0)
    return solucion

def greddy_tabu(lista_frecuencias):
    solucion = []
    for estacion in range(0,16):
        inversa = calcular_inversa(lista_frecuencias[estacion])
        suma_inversa = np.array(inversa).sum()
        divisiones = inversa / suma_inversa
        aleatorio = random.uniform(0,1)
        suma = 0
        for indice,valor in enumerate(divisiones):
            # print(indice , " ",valor)
            suma += valor
            if aleatorio < suma:
                inf = 5*indice
                sup = inf + 4
                nuevo_dato = random.randint(inf,sup)
                solucion.append(nuevo_dato)
                break
    return solucion


# s = [39, 25, 10, 14, 10, 11, 4, 5, 14, 8, 25, 27, 2, 9, 6, 11]
# lista_frecuencias = np.zeros([16,8])
# lista_frecuencias = actualizar_tabla_frecuencias(lista_frecuencias,s)
# # lista_frecuencias = actualizar_tabla_frecuencias(lista_frecuencias,s)
#
# print(s)
# greddy_tabu(lista_frecuencias)
# suma = np.array(inversa).sum()
#
# salida = inversa / suma
# print()
# print(salida)



# valor = 40
# if valor > 39:
#     indice_insercion = 7
# else:
#     indice_insercion = np.floor(valor / 5)
#
#
# print(indice_insercion)
# lista_frecuencias = np.zeros([16,8])
#
#
# for i in range(8):
#     r = randint(0,5)
#     lista_frecuencias[0][i] = r
#
# print(lista_frecuencias[0])
# inversa = np.reciprocal(lista_frecuencias[0],where= lista_frecuencias[0]!=0)
# print(inversa)
# suma = np.array(inversa).sum()
#
# salida = inversa / suma
# print()
# print(salida)


orden_numerico = np.arange(0, 17)

print(orden_numerico)