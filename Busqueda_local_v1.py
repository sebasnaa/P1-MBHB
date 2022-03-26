import itertools

import numpy as np
import random
import time

from random import randint
from numpy import genfromtxt




def modificar_datos_acciones(fichero_acciones):

    filas = fichero_acciones.shape[0]
    columnas = fichero_acciones.shape[1]
    salida = []
    for f in range(filas):
        for c in range(columnas):
            if not fichero_acciones[f][c] == 0:
                salida.append((c, fichero_acciones[f][c]))

    return salida

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

def greedy_inicializar(dimension,limite_elementos):

    arr = np.zeros(dimension)
    for i in range(limite_elementos):
        valor = randint(0, dimension)
        aux = valor % dimension
        arr[aux] += 1
    return arr

def estado_inicial_random():
    random_list = np.random.uniform(0, 1, 16)

    for indice in range(16):
        suma = np.array(random_list).sum()

        multiplicador = 219 - suma
        aux = random_list[indice] * multiplicador

        if (aux > 40):
            aux = np.random.uniform(0, 20, 1)

        random_list[indice] = aux

    random_list_rounded = np.round(random_list)
    slot_random = inicializar_greedy(random_list_rounded, 220)
    return slot_random

def inicializar_greedy(solucionInicial,limite_bicicletas):

    suma = np.array(solucionInicial).sum()
    multiplicador = limite_bicicletas/suma

    solucionInicial = np.array(solucionInicial)
    salida = solucionInicial*multiplicador
    salida_floor = np.floor(salida)
    salida_ceil = np.ceil(salida)
    if(np.array(salida_ceil).sum() < limite_bicicletas):
        return salida_ceil
    if(np.array(salida_floor).sum() < limite_bicicletas):
        return salida_floor

def generar_vecinos_no_offset(solucion_actual,limite_vecinos,granularidad):

    vecinos_generados = []
    for i in range(0,len(solucion_actual)):
        for j in range(i+1,len(solucion_actual)):

            if len(vecinos_generados) == limite_vecinos:
                break
            if i!=j:
                aux = solucion_actual.copy()
                if aux[i] > granularidad:
                    aux[i] -= granularidad
                    aux[j] += granularidad
                elif aux[j]> granularidad:
                    aux[i] += granularidad
                    aux[j] -= granularidad
                vecinos_generados.append(aux)
    return vecinos_generados


def generar_vecinos_con_offset(solucion_actual, limite_vecinos, granularidad):
    vecinos_generados = []
    orden_numerico = np.arange(0, solucion_actual.shape[0])
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
            aux[indiceA] -= granularidad
            aux[indiceB] += granularidad
        elif aux[indiceB] > granularidad:
            aux[indiceA] += granularidad
            aux[indiceB] -= granularidad

        vecinos_generados.append(aux)
        i += 1
        if i == tam:
            break
    return vecinos_generados



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

def coste_slot(slots):
    # Ajustamos el vector de slots al primer movimiento que tenemos que cubrir
    distanciaTotal = 0
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

    return distanciaTotal









############################## Programa final ###############################
################## Inicializar variables ficheros



indices = genfromtxt('datos/cercanas_indices.csv', delimiter=',')
indicesMod = np.delete(indices, 0, 0)

kmRelativos = genfromtxt('datos/cercanas_kms.csv', delimiter=',')
kmRelativosMod = np.delete(kmRelativos, 0, 0)

acciones = genfromtxt('datos/deltas_5m.csv', delimiter=',')
bicicletas_objetivo_iniciales = acciones[1]
accionesMod = np.delete(acciones, 0, 0)
accionesMod = np.delete(accionesMod, 0, 0)

lista_acciones = modificar_datos_acciones(accionesMod*2)

coste_maximo = 99999999999999999
for indice_semilla in range(1):

    ################## Inicializar variables bucles
    iteraciones = 0
    #Se genera la solucion actual inicial
    # slot_por_estaciones = greedy_inicializar(16, 220)
    slot_por_estaciones = np.array([19, 12, 16, 18, 16, 11, 17,  8, 14, 15, 18, 16,  7,  8, 12, 13,])
    bicicletas_disponibles = np.zeros(slot_por_estaciones.size)
    huecos_disponibles = slot_por_estaciones - bicicletas_disponibles
    coste_mejor = coste_slot(slot_por_estaciones)
    print("#",indice_semilla , " " , slot_por_estaciones , " coste ", coste_mejor)
    numero_veces_mejora_coste = 0
    no_encuentra = False
    start_time = time.time()

    while not no_encuentra and iteraciones < 5:
        # vecinos = generar_vecinos_no_offset(slot_por_estaciones,120,2)
        vecinos = generar_vecinos_con_offset(slot_por_estaciones,240,4 )
        k = 0
        for v in vecinos:
            aux = v.copy()
            bicicletas_disponibles = np.zeros(aux.size)
            huecos_disponibles = aux - bicicletas_disponibles
            coste_tmp = coste_slot(aux)
            k +=1
            # print("costes tmp #",iteraciones , " #",k ," " , coste_tmp , " coste mejor " , coste_mejor)
            if coste_tmp < coste_mejor:
                numero_veces_mejora_coste += 1
                slot_por_estaciones = aux.copy()
                coste_mejor = coste_tmp

                break
            else:
                if k == len(vecinos):
                    print(k, " llega limite")
                    no_encuentra = True

        iteraciones+=1


    if (coste_mejor < coste_maximo):
        coste_maximo = coste_mejor
    print(slot_por_estaciones , "coste mejor ",coste_mejor , " nº mejoras " , numero_veces_mejora_coste , " " , "--- %s seconds ---" % (time.time() - start_time))


print("coste maximo " , coste_maximo)
# a = greedy_inicializar(16,220)
# vecinos = generar_vecinos_no_offset(a,20,1)













