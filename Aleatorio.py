import math
import random
from builtins import print
from pickletools import dis
from random import randint

import numpy as np
import time

from numpy import genfromtxt



def modificar_datos_acciones(ficheroAcciones):

    filas = ficheroAcciones.shape[0]
    columnas = ficheroAcciones.shape[1]
    salida = []
    for f in range(filas):
        for c in range(columnas):
            if not ficheroAcciones[f][c] == 0:
                salida.append((c, ficheroAcciones[f][c]))

    return salida

#
def estado_inicial_random():
    random_list = np.random.uniform(0, 1, 16)

    for indice in range(16):
        suma = np.array(random_list).sum()

        multiplicador = 218 - suma
        aux = random_list[indice] * multiplicador

        if (aux > 50):
            aux = np.random.uniform(0, 50, 1)

        random_list[indice] = aux

    random_list_rounded = np.round(random_list)
    slot_random = inicializar_greedy(random_list_rounded, 218)
    return slot_random
#

def inicializar_greedy(solucionInicial,limite_bicicletas):

    suma = np.array(solucionInicial).sum()
    multiplicador = limite_bicicletas/suma

    solucionInicial = np.array(solucionInicial)
    salida = solucionInicial*multiplicador

    salida = np.array(salida).round()
    return salida


    # if(np.array(salida_ceil).sum() < limite_bicicletas):
    #     return salida_ceil
    # if(np.array(salida_floor).sum() < limite_bicicletas):
    #     return salida_floor


def inicializar_solucion_homogenea(dimension,limite_elementos):

    arr = np.zeros(dimension)
    for i in range(limite_elementos):
        valor = randint(0, dimension)
        aux = valor % dimension
        arr[aux] += 1
    return arr



def accion_posible(bicicletas_input,estacion):
    # queremos guardar bicis
    # estacion =  estacion -1
    if(bicicletas_input>0):
        if huecos_disponibles[estacion] >= bicicletas_input:
            bicicletas_disponibles[estacion] = bicicletas_disponibles[estacion]+bicicletas_input
            huecos_disponibles[estacion] = huecos_disponibles[estacion]-bicicletas_input
            return 0
        elif huecos_disponibles[estacion] >0:
            while huecos_disponibles[estacion] > 0:
                bicicletas_input = bicicletas_input-1
                bicicletas_disponibles[estacion] = bicicletas_disponibles[estacion] + 1
                huecos_disponibles[estacion] = huecos_disponibles[estacion] - 1
            return bicicletas_input
        else:
            return bicicletas_input
    else:
        #queremos sacar bicis
        #se utiliza un valor negativo en bicicletas_input por tanto *-1
        aux = (bicicletas_input *(-1))
        if bicicletas_disponibles[estacion] >= aux:
            #se suma un valor neg por tanto se resta
            bicicletas_disponibles[estacion] = bicicletas_disponibles[estacion]-aux
            #se resta un valor neg por tanto se suma
            huecos_disponibles[estacion] = huecos_disponibles[estacion]+aux


            return 0
        elif bicicletas_disponibles[estacion] > 0:
            while bicicletas_disponibles[estacion] >0:
                bicicletas_disponibles[estacion] = bicicletas_disponibles[estacion]-1
                huecos_disponibles[estacion]  = huecos_disponibles[estacion] + 1
                bicicletas_input+=1

            return bicicletas_input
        else:
            return bicicletas_input


def estacion_cercana(estacion,bicicletas):
    estacion_actual = estacion
    bicicletas_input = bicicletas

    indice_busqueda = 1
    estacion_encontrada = False

    estacion_siguiente = -1
    distancia_Nan = 0
    #queremos buscar una estacion cercana con posibilidad de guardar alguna bici
    if bicicletas_input > 0:
        while not estacion_encontrada:

            indice_estacion_cercana = indicesMod[estacion_actual][indice_busqueda]
            indice_estacion_cercana = int(indice_estacion_cercana)
            if huecos_disponibles[indice_estacion_cercana] != 0:
                estacion_siguiente =  indice_estacion_cercana
                distancia_Nan = kmRelativosMod[estacion_actual][indice_busqueda]
                estacion_encontrada = True
            indice_busqueda+=1
        return bicicletas_input,estacion_siguiente, distancia_Nan
    else:
        while not estacion_encontrada:
            indice_estacion_cercana = indicesMod[estacion_actual][indice_busqueda]
            indice_estacion_cercana = int(indice_estacion_cercana)
            if bicicletas_disponibles[indice_estacion_cercana] != 0:
                estacion_siguiente =  indice_estacion_cercana
                distancia_Nan = kmRelativosMod[estacion_actual][indice_busqueda] * 3
                estacion_encontrada = True
            indice_busqueda+=1
        return bicicletas_input,estacion_siguiente, distancia_Nan

def generar_vecinos_random(slots,valor_cambio):
    modificado = False
    while(not modificado):

        indiceA = random.randint(0,15)
        indiceB = random.randint(0,15)
        while(indiceA == indiceB):
            indiceB = random.randint(0, 15)

        if(slots[indiceA] > valor_cambio):
            slots[indiceA] -= valor_cambio
            slots[indiceB] += valor_cambio
            modificado = True
        elif(slots[indiceB] > valor_cambio):
            slots[indiceB] -= valor_cambio
            slots[indiceA] += valor_cambio
            modificado = True
    return slots




############################## Programa final ###############################

################## Inicializar variables



indices = genfromtxt('datos/cercanas_indices.csv', delimiter=',')
indicesMod = np.delete(indices, 0, 0)

kmRelativos = genfromtxt('datos/cercanas_kms.csv', delimiter=',')
kmRelativosMod = np.delete(kmRelativos, 0, 0)

acciones = genfromtxt('datos/deltas_5m.csv', delimiter=',')
bicicletas_objetivo_iniciales = acciones[1]
accionesMod = np.delete(acciones, 0, 0)
accionesMod = np.delete(accionesMod, 0, 0)

lista_acciones = modificar_datos_acciones(accionesMod*2)

numero_semillas = 1
coste_minimo = math.inf
solucion_minima = []


for indice_semilla in range(numero_semillas):

    # slot_por_estaciones = inicializar_solucion_homogenea(16,220)
    # # slot_por_estaciones = estado_inicial_random()
    # bicicletas_disponibles = np.zeros(slot_por_estaciones.size)
    #
    # huecos_disponibles = slot_por_estaciones - bicicletas_disponibles
    # distanciaTotal = 0

    start_time = time.time()
    coste_minimo = math.inf

    for repeticiones in range(1):

        # slot_por_estaciones = estado_inicial_random()
        # slot_por_estaciones = inicializar_greedy(slot_por_estaciones, 220)


        slot_por_estaciones = inicializar_solucion_homogenea(16, 220)


        print(np.array(slot_por_estaciones).sum())
        bicicletas_disponibles = np.zeros(slot_por_estaciones.size)

        huecos_disponibles = slot_por_estaciones - bicicletas_disponibles

        solucion_minima = slot_por_estaciones
        distanciaTotal = 0


        #Ajustamos el vector de slots al primer movimiento que tenemos que cubrir
        for i in range(np.array(indices).shape[1]):
            estacion = i
            bicicletas = bicicletas_objetivo_iniciales[i]
            out = (accion_posible(bicicletas, estacion))
            while out != 0:
                out, estacion_sig, distancia_aux = estacion_cercana(estacion, out)
                out = (accion_posible(out, estacion_sig))

        for indice in range(np.array(lista_acciones).shape[0]):
            acc = lista_acciones[indice]
            estacion = acc[0]
            bicicletas = acc[1]
            out = (accion_posible(bicicletas, estacion))
            while out != 0:

                bicis_res, estacion_sig, distancia_aux = estacion_cercana(estacion, out)
                out = (accion_posible(bicis_res, estacion_sig))
                tmp = abs(bicis_res) - abs(out)
                distanciaTotal = distanciaTotal + distancia_aux*tmp

        if(distanciaTotal < coste_minimo):
            coste_minimo = distanciaTotal
            solucion_minima = slot_por_estaciones
        # print("\n  semilla @"  ,indice_semilla  ," repeticion#" , repeticiones, distanciaTotal , slot_por_estaciones)
    print("Sol #", indice_semilla , " ", solucion_minima, " distancia minima ", coste_minimo, "suma ", np.array(slot_por_estaciones).sum()," --- %s seconds ---" % (time.time() - start_time))
# print( "Sol " ,solucion_minima ," distancia minima " , coste_minimo ,    "suma "  , np.array(slot_por_estaciones).sum()  ,    " --- %s seconds ---" % (time.time() - start_time))