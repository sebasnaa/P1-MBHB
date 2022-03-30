import itertools
import math

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
    multiplicador = limite_bicicletas / suma

    solucionInicial = np.array(solucionInicial)
    salida = solucionInicial * multiplicador

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

    solucion = inicializar_greedy(solucion,220)
    return solucion




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

coste_maximo = math.inf


################## Inicializar variables bucles
iteraciones = 0
#Se genera la solucion actual inicial
# s_act = np.array([39, 25, 10, 14, 10, 11, 4, 5, 14, 8, 25, 27, 2, 9, 6, 11])
s_act = greedy_inicializar(16, 220)


bicicletas_disponibles = np.zeros(s_act.size)
huecos_disponibles = s_act - bicicletas_disponibles
coste_minimo = coste_slot(s_act)
coste_s_act = coste_minimo
solucion_minima = s_act.copy()
start_time = time.time()


# posicion valor
# van de dos en dos

movimiento_mejor_vecino = []
mejor_vecino = []



lista_tabu = []
longitud_lista_tabu_limite = 2
duracion = 3
indice_agregacion = 0
lista_frecuencias = np.zeros([16,8])




print("##Coste solucion inicial ", coste_s_act)
while iteraciones < 4000:

    if iteraciones % 1000 == 0 and iteraciones > 0:
        r = random.uniform(0,1)
        print("segundo")
        s_act = greddy_tabu(lista_frecuencias)
        # print(s_act)
        print(np.array(s_act).sum())
        # if(r < 0.25):
        #     # reinicializar completo
        #     print("primero")
        #     s_act = greedy_inicializar(16, 220)
        #     coste_minimo = coste_slot(s_act)
        #     coste_s_act = coste_minimo
        # if(r >= 0.25 and r < 0.75):
        #     print("segundo")
        #     s_act = greddy_tabu(lista_frecuencias)
        #     # print(s_act)
        #     print(np.array(s_act).sum())
        # if(r >= 0.75):
        #     print("tercero")
        #     s_act = solucion_minima.copy()
        #     coste_minimo = coste_slot(s_act)
        #     coste_s_act = coste_minimo


    s_act = np.array(s_act)
    print(s_act)
    vecinos,movimientos = generar_vecinos_con_offset(s_act,40,2 )
    mejor_vecino = vecinos[0]
    coste_mejor_vecino = coste_slot(mejor_vecino)
    movimiento_actual = movimientos[0]



    k = 0
    # print("Coste interno iteracion #",iteraciones ,"  " , coste_slot(s_act))
    # print("Lista tabu " , lista_tabu)
    for v in vecinos:

        s_cand = v.copy()
        bicicletas_disponibles = np.zeros(s_cand.size)
        huecos_disponibles = s_cand - bicicletas_disponibles
        coste_cand = coste_slot(s_cand)

        if coste_cand < coste_mejor_vecino:
            coste_mejor_vecino = coste_cand
            mejor_vecino = s_cand.copy()
            movimiento_actual = movimientos[k]

        #criterio de aspiracion, es mejor el vecino que la solucion_mejor,
        # no se tiene en cuenta que estuviera en la lista_tabu no importa
        if coste_cand < coste_minimo:
            solucion_minima = s_cand.copy()
            s_act = s_cand.copy()
            movimiento_actual = movimientos[k].copy()
            # print("         mejoro coste, cumplo criterio de aspiracion", movimiento_actual ,  " coste anterior " , coste_minimo  , " coste " , coste_cand)
            coste_minimo = coste_cand

        if not existe_movimiento_tabu(lista_tabu,movimiento_actual):
            if coste_cand < coste_s_act:
                # print("         mejoro coste  y no estoy en lista tabu " , movimiento_actual)
                movimiento_actual = movimientos[k].copy()
                s_act = s_cand.copy()
        k+=1
    # print("mejor de los vecinos " , mejor_vecino , " mov ",movimiento_actual )
    # print("++agrego en lista tabu++")

    lista_tabu,indice_agregacion = agregar_lista_tabu(lista_tabu,movimiento_actual,longitud_lista_tabu_limite,duracion, indice_agregacion)
    lista_frecuencias = actualizar_tabla_frecuencias(lista_frecuencias,s_act)
    lista_tabu = reducir_tiempo_lista_tabu(lista_tabu)
    iteraciones+=1
    print("#",iteraciones)

print(" solucion mejor " , solucion_minima , " coste ", coste_minimo , "--- %s seconds ---" % (time.time() - start_time))














