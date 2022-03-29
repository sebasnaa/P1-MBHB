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

def accion_posible(bicicletas_input,estacion,bicicletas_en_slots,huecos_disponibles_en_slots):
    # queremos guardar bicis
    # estacion =  estacion -1
    if(bicicletas_input>0):
        if huecos_disponibles_en_slots[estacion] >= bicicletas_input:
            bicicletas_en_slots[estacion] = bicicletas_en_slots[estacion]+bicicletas_input
            huecos_disponibles_en_slots[estacion] = huecos_disponibles_en_slots[estacion]-bicicletas_input
            return 0,bicicletas_en_slots,huecos_disponibles_en_slots
        elif huecos_disponibles_en_slots[estacion] >0:
            while huecos_disponibles_en_slots[estacion] > 0:
                bicicletas_input = bicicletas_input-1
                bicicletas_en_slots[estacion] = bicicletas_en_slots[estacion] + 1
                huecos_disponibles_en_slots[estacion] = huecos_disponibles_en_slots[estacion] - 1
            return bicicletas_input,bicicletas_en_slots,huecos_disponibles_en_slots
        else:
            return bicicletas_input,bicicletas_en_slots,huecos_disponibles_en_slots
    else:
        #queremos sacar bicis
        #se utiliza un valor negativo en bicicletas_input por tanto *-1
        aux = (bicicletas_input *(-1))
        if bicicletas_en_slots[estacion] >= aux:
            #se suma un valor neg por tanto se resta
            bicicletas_en_slots[estacion] = bicicletas_en_slots[estacion]-aux
            #se resta un valor neg por tanto se suma
            huecos_disponibles_en_slots[estacion] = huecos_disponibles_en_slots[estacion]+aux


            return 0,bicicletas_en_slots,huecos_disponibles_en_slots
        elif bicicletas_en_slots[estacion] > 0:
            while bicicletas_en_slots[estacion] >0:
                bicicletas_en_slots[estacion] = bicicletas_en_slots[estacion]-1
                huecos_disponibles_en_slots[estacion]  = huecos_disponibles_en_slots[estacion] + 1
                bicicletas_input+=1

            return bicicletas_input,bicicletas_en_slots,huecos_disponibles_en_slots
        else:
            return bicicletas_input,bicicletas_en_slots,huecos_disponibles_en_slots

def estacion_cercana(estacion,bicicletas,bicicletas_en_slots,huecos_disponibles_en_slots):
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
            if huecos_disponibles_en_slots[indice_estacion_cercana] != 0:
                estacion_siguiente =  indice_estacion_cercana
                distancia_Nan = kmRelativosMod[estacion_actual][indice_busqueda]
                estacion_encontrada = True
            indice_busqueda+=1
        return bicicletas_input,estacion_siguiente, distancia_Nan
    else:
        while not estacion_encontrada:
            indice_estacion_cercana = indicesMod[estacion_actual][indice_busqueda]
            indice_estacion_cercana = int(indice_estacion_cercana)
            if bicicletas_en_slots[indice_estacion_cercana] != 0:
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

        multiplicador = 218 - suma
        aux = random_list[indice] * multiplicador

        if (aux > 50):
            aux = np.random.uniform(0, 50, 1)

        random_list[indice] = aux

    random_list_rounded = np.round(random_list)
    slot_random = inicializar_greedy(random_list_rounded, 218)
    return slot_random

def inicializar_greedy(solucionInicial,limite_bicicletas):

    suma = np.array(solucionInicial).sum()
    multiplicador = limite_bicicletas/suma

    solucionInicial = np.array(solucionInicial)
    salida = solucionInicial*multiplicador

    salida = np.array(salida).round()
    return salida

    # salida_floor = np.floor(salida)
    # salida_ceil = np.ceil(salida)
    # if(np.array(salida_ceil).sum() < limite_bicicletas):
    #     return salida_ceil
    # if(np.array(salida_floor).sum() < limite_bicicletas):
    #     return salida_floor

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

def generar_vecinos_con_offset_punto(solucion_actual, limite_vecinos, granularidad,punto_partida):
    vecinos_generados = []
    orden_numerico = np.arange(0, solucion_actual.shape[0])
    lista_permutaciones_posibles = itertools.permutations(orden_numerico, 2)
    lista_permutaciones_posibles = list(lista_permutaciones_posibles)
    # np.random.shuffle(lista_permutaciones_posibles)
    # if limite_vecinos > 240:
    #     limite_vecinos = 240

    i = punto_partida % 240


    contador = 0
    while contador < limite_vecinos:
        # print("valor contador interno ", i)
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
        i = i + 1
        i = i % 240
        contador+=1
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

def coste_slot(slot_por_estaciones):
    # Ajustamos el vector de slots al primer movimiento que tenemos que cubrir
    distanciaTotal = 0
    bicicletas_disponibles = np.zeros(slot_por_estaciones.size)
    huecos_disponibles = slot_por_estaciones - bicicletas_disponibles
    for i in range(np.array(indices).shape[1]):
        estacion = i
        bicicletas = bicicletas_objetivo_iniciales[i]
        out,bicicletas_disponibles,huecos_disponibles = (accion_posible(bicicletas, estacion,bicicletas_disponibles,huecos_disponibles))
        while out != 0:
            out, estacion_sig, distancia_aux = estacion_cercana(estacion, out,bicicletas_disponibles,huecos_disponibles)
            out, bicicletas_disponibles, huecos_disponibles = accion_posible(out, estacion_sig,bicicletas_disponibles,huecos_disponibles)

    for indice in range(np.array(lista_acciones).shape[0]):
        acc = lista_acciones[indice]
        estacion = acc[0]
        bicicletas = acc[1]
        out, bicicletas_disponibles, huecos_disponibles = accion_posible(bicicletas, estacion,bicicletas_disponibles,huecos_disponibles)
        while out != 0:
            bicis_res, estacion_sig, distancia_aux = estacion_cercana(estacion, out,bicicletas_disponibles,huecos_disponibles)
            out, bicicletas_disponibles, huecos_disponibles = (accion_posible(bicis_res, estacion_sig,bicicletas_disponibles,huecos_disponibles))

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

mejor_slot = []
for indice_semilla in range(200):

    # slot_por_estaciones = inicializar_greedy([5, 7, 13, 6, 8, 13, 8, 9, 6, 10, 10, 18, 8, 13, 15, 14], 220)
    # bicicletas_disponibles = [5, 7, 13, 6, 8, 13, 8, 9, 6, 10, 10, 18, 8, 13, 15, 14]
    ################## Inicializar variables bucles
    iteraciones = 0
    #Se genera la solucion actual inicial
    # slot_por_estaciones = np.array([39, 25, 10, 14, 10, 11, 4, 5, 14, 8, 25, 27, 2, 9, 6, 11])
    # slot_por_estaciones = np.array([17, 12, 20, 20, 20, 14, 9, 12, 11, 14, 12, 23, 2, 9, 12, 13])

    slot_por_estaciones = estado_inicial_random()
    print( " suma " , np.array(slot_por_estaciones).sum())
    np.random.shuffle(slot_por_estaciones)

    bicicletas_disponibles = np.zeros(slot_por_estaciones.size)
    huecos_disponibles = slot_por_estaciones - bicicletas_disponibles
    coste_mejor = coste_slot(slot_por_estaciones)
    print(" coste asdas ",coste_mejor)
    print("#",indice_semilla , " " , slot_por_estaciones , " coste ", coste_mejor)
    no_encuentra = False
    mejora = False
    start_time = time.time()
    vecinos_totales = 240
    r = random.randint(0, 240)
    offset = r % 240

    k = 0
    while not no_encuentra and iteraciones < 3000:
        # print(" iteraccion #",iteraciones)
        # vecinos = generar_vecinos_no_offset(slot_por_estaciones,120,2)
        lotes_size = 20
        paso = 2
        vecinos = generar_vecinos_con_offset_punto(slot_por_estaciones,lotes_size,paso,offset)
        for v in vecinos:
            # print( " entrada #",k , " veces en comprobar vecinos")
            aux = v.copy()
            bicicletas_disponibles = np.zeros(aux.size)
            huecos_disponibles = aux - bicicletas_disponibles
            coste_tmp = coste_slot(aux)
            vecinos_totales -= 1
            mejora = False
            if coste_tmp < coste_mejor:
                k += 1
                slot_por_estaciones = aux.copy()
                coste_mejor = coste_tmp
                r = random.randint(0, 240)
                offset = r
                # print("Encuentra mejor en " ,k, " ,reinicio , nuevo random " , offset , " vecinos restante ", vecinos_totales)
                vecinos_totales = 240
                mejora = True
                if coste_mejor < coste_maximo:
                    coste_maximo = coste_mejor
                    mejor_slot = slot_por_estaciones.copy()
                break

            if vecinos_totales == 0:
                    # print(" llega limite")
                    no_encuentra = True
        iteraciones+=1
        if not mejora:
            offset+= lotes_size
            mejora = False

    print(slot_por_estaciones , "coste mejor ",coste_mejor ,  " mejoras " , k    ," " , "--- %s seconds ---" % (time.time() - start_time))


print(mejor_slot," coste maximo " , coste_maximo , " " , np.array(mejor_slot).sum())













