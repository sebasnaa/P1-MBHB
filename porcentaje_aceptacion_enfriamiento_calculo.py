import itertools
import math
import matplotlib.pyplot as plt
import numpy as np
import random
import time

from random import randint
from numpy import genfromtxt
from math import log



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

def inicializar_solucion_homogenea(dimension,limite_elementos):

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

def temperatura_inicial(coste_inicial):
    t = 0
    a = 0.3
    b = 0.09

    t = a/(-log(b))
    t=t*coste_inicial
    return t



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

minimos = []

################## Inicializar variables bucles

#Se genera la solucion actual inicial
# s_actual = np.array([39, 25, 10, 14, 10, 11, 4, 5, 14, 8, 25, 27, 2, 9, 6, 11] )

media_aceptados = 0
minima_solucion_coste = 99999999999999999999999
minima_solucion_slots = []

seeds = [
[36, 10, 12,  7, 17, 15, 14,  8,  9, 17,  8, 18, 13, 12, 13, 11,],
[27, 10, 10, 18,  9, 15, 15, 15, 14, 10, 17, 13, 13, 14,  9, 11,],
[25, 15,  9, 10, 14, 12, 15, 14,  9, 14, 15, 12,  9, 15, 18, 14,],
[27, 12,  9, 13, 12, 18, 22, 16, 11,  9,  7, 12, 11, 11, 12, 18,],
[26, 15, 12,  9,  9, 12, 13, 10, 24, 15,  9, 14, 12, 11, 12, 17,]
]


# for pruebas in range(5):

for seed in range(10):
    total_comprobados = 0
    total_aceptados = 0

    # s_actual = np.array(seeds[pruebas])

    s_actual = inicializar_solucion_homogenea(16,220)

    # s_actual = estado_inicial_random()
    np.random.shuffle(s_actual)

    bicicletas_disponibles = np.zeros(s_actual.size)

    coste_minimo = coste_slot(s_actual)
    mejor_solucion = s_actual.copy()
    start_time = time.time()

    temperatura_ini  = temperatura_inicial(coste_minimo)
    iteraciones = 0
    k = 0
    numero_mejoras = []
    eje_y = []
    eje_x = []
    numero_aceptados = []
    array_temperaturas = []
    temperatura = temperatura_ini

    # condicion de parada
    while iteraciones in range(100):
        # print("#", iteraciones , " temperatura " , temperatura)
        # Condicion de enfriamiento numero de enfriamientos que se haran por jemplo 20 descensos
        # se realiza cuando se han comprobado los vecinos sin importar si se han aceptado o no
        eje_x.append(iteraciones)
        eje_y.append(temperatura)
        array_temperaturas.append(temperatura)
        sumatorio = 0
        for ite_v_enfriamiento in range(1):
            total_comprobados+= 1
            # vecinos = generar_vecinos_no_offset(slot_por_estaciones,120,2)
            vecinos = generar_vecinos_con_offset(s_actual,1,1)
            s_cand = vecinos[0]

            # coste_s_actual = coste_slot(s_actual)
            coste_s_actual = 574
            coste_s_cand = coste_slot(s_cand)
            diff = (coste_s_cand - coste_s_actual)
            # diff = round(diff, 2)
            # temperatura = round(temperatura, 2)
            # print( " .............................  ", diff  , "   " , temperatura)

            criterio =  np.exp(-diff/temperatura)
            probabilidad  = random.uniform(0,1)
            # print( "ite ",ite_v_enfriamiento , " criterio " , criterio , " probabilidad " , probabilidad)
            if(probabilidad < criterio or diff < 0):
                s_actual = s_cand
                sumatorio+=1
                total_aceptados+=1
                # print("Aceptp solucion " , " coste actual " ,coste_s_actual , " coste candidato " , coste_s_cand )
                if(coste_s_cand < coste_minimo):
                    coste_minimo = coste_s_cand
                    mejor_solucion = s_cand.copy()
                    if(coste_minimo < minima_solucion_coste):
                        minima_solucion_coste = coste_minimo
                        minima_solucion_slots = s_cand.copy()

        numero_aceptados.append(sumatorio)
        k+=1
        temperatura = temperatura_ini / (1+k)

        # temperatura = 0.95*temperatura
        iteraciones+=1


    print(mejor_solucion , "coste mejor ",coste_minimo , "--- %s seconds ---" % (time.time() - start_time))
    # minimos.append(coste_minimo)
    print(" total comprobados  ", total_comprobados , " total aceptados ", total_aceptados , " porcentaje aceptados " , (total_aceptados/total_comprobados)*100,"%")
    media_aceptados+=(total_aceptados/total_comprobados)*100

print("coste " , minima_solucion_coste , " slots " , minima_solucion_slots,  "  " , np.array(minima_solucion_slots).sum())
print(media_aceptados/10)

# print(np.array(minimos).min())

# eje_x = np.array(eje_x)
# eje_y = np.array(eje_y)
# # # print(eje_y)
# # print(eje_x)
# plt.plot(eje_x,eje_y)
# plt.show()

#
# print(np.array(array_temperaturas))
# print(np.array(numero_aceptados))
#
# intervalos = range(min(numero_aceptados), max(numero_aceptados) + 1)
# plt.hist(numero_aceptados, intervalos,rwidth=0.9)
# plt.title('  Aceptaciones/Temperatura ')
# plt.xlabel('numero aceptados')
# plt.ylabel('Temperatura')
# plt.xticks(intervalos)


# plt.plot(numero_aceptados,array_temperaturas)
# plt.xlabel(' Aceptados')
# plt.ylabel('Tempratura')
# plt.show()

