# -*- coding: utf-8 -*-
"""
Created on ??

@author: Luis
"""

from random import randint, expovariate, random
from cargar_modelo_comp import Prediccion_Preferencias
from logit import calculo_probs
from importar_datos import importar_casas
from documentar import Documentador, Docu2
from numpy.random import choice
from numpy import cumsum

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
predictor = Prediccion_Preferencias()


class Persona:


    def __init__(self, tipo):
        self.tipo = tipo
        self.determinar_preferencias()

    def determinar_preferencias(self):
        self.preferencias = predictor.entregar_preferencias(self.tipo-1)


class Casa:


    def __init__(self, identificador, atributos, precio):
        self.identificador = identificador
        self.atributos = atributos
        self.precio = precio
        self.precio_inicial = precio
        self.precio_anterior = precio
        self.precio_minimo = 0
        self._vendida = False
        #Estas variables sirven al momento de atender un cliente
        self.utilidad = 0
        self.probabilidad = 0


    @property
    def vendida(self):
        return self._vendida

    @vendida.setter
    def vendida(self, valor):
        self._vendida = True
        self.precio_venta = valor

    def cambiar_precio(self, coeficiente):
        self.precio = coeficiente * self.precio
        if self.precio >= self.precio_inicial:
            self.precio = self.precio_inicial


class Inmobiliaria:


    def __init__(self, alfa, coef, no_compra):
        self.precios_casas_vendidas = [] #lista de tuplas, primera posición idcasa, segunda posición precio casa
        self.cantidad_personas_no_compran = 0
        self.factor_precios_por_casa_para_cada_periodo = [[] for i in range(100)]
        self.precios_por_casa_para_cada_periodo = [[] for i in range(100)]
        self.nombre = "Inmobiliaria S.A"
        atributos = importar_casas(alfa)
        self.coef = coef
        self.no_compra = no_compra
        self.casas = []
        for i in range(0, 100):
            """ Agregamos los precios de las casa del excel"""
            casita = Casa(atributos[i][0], atributos[i][1:15], atributos[i][15])
            self.casas.append(casita)
            self.factor_precios_por_casa_para_cada_periodo[i].append(casita.precio/casita.precio_inicial)
            self.precios_por_casa_para_cada_periodo[i].append(casita.precio)

    def atender(self, cliente, documentador, tiempo):
        tuplas = list()
        casas_disponibles = list()
        for i in self.casas:
            if not i.vendida:
                """Se concatenan los atributos de la casa con las preferencias 
                del cliente, luego se hacen tuplas con el precio y la prediccion
                y finalmente se calculan las probabilidades de no compra."""
                casas_disponibles.append(i)
                test = i.atributos + cliente.preferencias
                tupla = (i.precio, predictor.prediccion(test)[0])
                tuplas.append(tupla)
        utis, probs = calculo_probs(tuplas, self.coef, self.no_compra)

        """Asignamos a cada casa su correspondiente utlidad y 
        probabilidad de no compra"""
        for i in range(len(casas_disponibles)):
            casas_disponibles[i].utilidad = utis[i]
        #Se ordenan las casas segun su utilidad de mayor a menor
        casas_disponibles = sorted(casas_disponibles, key=lambda x: x.utilidad, reverse=True)
        """Comprobamos con las primeras 5 (se puede cambiar) casas si alguna se vende"""
        tuplas = []
        casas_ofrecidas = []
        for i in range(min(5, len(casas_disponibles))):
            casas_ofrecidas.append(casas_disponibles[i])
            test = casas_disponibles[i].atributos + cliente.preferencias
            tuplas.append((predictor.prediccion(test)[0], casas_disponibles[i].precio))
        utis2, probs2 = calculo_probs(tuplas, self.coef, self.no_compra)
        casas_ofrecidas.append("Negative")
        value = random()
        for i in range(len(probs2)):
            lista_limites = cumsum(probs2)
        if 0 <= value <= lista_limites[0]:
            draw = casas_ofrecidas[0]
        elif lista_limites[0] < value <= lista_limites[1]:
            draw = casas_ofrecidas[1]
        elif lista_limites[1] < value <= lista_limites[2]:
            draw = casas_ofrecidas[2]
        elif lista_limites[2] < value <= lista_limites[3]:
            draw = casas_ofrecidas[3]
        elif lista_limites[3] < value <= lista_limites[4]:
            draw = casas_ofrecidas[4]
        else:
            draw = casas_ofrecidas[5]
        if draw == "Negative":
            self.cantidad_personas_no_compran += 1
        else:
            for c in range(len(casas_disponibles)):
                if casas_disponibles[c] == draw:
                    documentador.casa_vendida(casas_disponibles[c], tiempo, cliente.tipo)
                    self.precios_casas_vendidas.append((casas_disponibles[c].identificador, casas_disponibles[c].precio))
                    casas_disponibles[c].vendida = True
                    break


class Simulacion:


    def __init__(self, tiempo_maximo, tasa_llegada, alfa, coef, no_compra,
                 cambio, tolerancia_cambio):
        self.tiempo_maximo_sim = tiempo_maximo
        self.tasa_llegada_clientes = tasa_llegada
        self.tiempo_simulacion = 1
        self.inmobiliaria = Inmobiliaria(alfa, coef, no_compra)
        self.clientes_tipo1_atendidos = 0
        self.clientes_tipo2_atendidos = 0
        self.clientes_tipo3_atendidos = 0
        self.clientes_tipo4_atendidos = 0
        self.clientes_perdidos = 0
        self.tolerancia_cambio = tolerancia_cambio
        self.resultados = Documentador(self.inmobiliaria)
        self.t_cambios = [i * 7 * 24  for i in cambio]
        self.semana_period_anter = 0
        self.nro_casas_antes = 100

    def llegadas_clientes(self, tasa_llegada):
        tiempos_entre_llegada_clientes = [round(expovariate(tasa_llegada))]
        while sum(tiempos_entre_llegada_clientes) <= self.tiempo_maximo_sim:
            tiempos_entre_llegada_clientes.append(round(expovariate(tasa_llegada)))
        tiempos_entre_llegada_clientes.pop()
        self.tiempos_llegada_clientes = [sum(tiempos_entre_llegada_clientes[:i]) for i in \
                                    range(len(tiempos_entre_llegada_clientes)+1)][1::]

    def actualizar_precios(self, semana):
        semana = semana /(7*24)
        num_vendidas = len([i for i in self.inmobiliaria.casas if i.vendida])
        factor = num_vendidas/semana
        if factor >= 1 + self.tolerancia_cambio:
            factor = 1 + self.tolerancia_cambio
        elif factor <= 1 - self.tolerancia_cambio:
            factor = 1 - self.tolerancia_cambio
        for casa in self.inmobiliaria.casas:
            if not casa.vendida:
                casa.cambiar_precio(factor)

    def run(self):
        """Este metodo ejecuta la simulacion de la inmobiliaria
        se estima aleatoreamente la llegada de clientes"""
        self.llegadas_clientes(self.tasa_llegada_clientes)
        self.resultados.cambio_precio(0)
        """Ejecutamos el ciclo verificando que el tiempo de simulacion no supere
        el tiempo maximo de simulacion"""
        while self.tiempo_simulacion <= self.tiempo_maximo_sim:
            """Verificamos si en el tiempo actual(día) de la simulación llega algún cliente"""
            if not(self.tiempo_simulacion in self.tiempos_llegada_clientes):
                pass
            if (self.tiempo_simulacion in self.t_cambios):
                self.actualizar_precios(self.tiempo_simulacion)
                self.resultados.cambio_precio(self.tiempo_simulacion / (7 * 24))
                for i in range(0, 100):
                    factor_precio = self.inmobiliaria.casas[i].precio / self.inmobiliaria.casas[i].precio_inicial
                    self.inmobiliaria.factor_precios_por_casa_para_cada_periodo[i].append(factor_precio)
                    self.inmobiliaria.precios_por_casa_para_cada_periodo[i].append(self.inmobiliaria.casas[i].precio)
            else:
                text = "[HORA {}]: Llega(n) ".format(self.tiempo_simulacion)
                for i in range(self.tiempos_llegada_clientes.count(self.tiempo_simulacion)):
                    value = random() #Con esto verificamos de que tipo es el cliente
                    if value <= 0.432:
                        text += "Cliente tipo 1 "
                        nuevo_cliente = Persona(1)
                        self.inmobiliaria.atender(nuevo_cliente, self.resultados, self.tiempo_simulacion)
                    elif value <= 0.724:
                        text += "Cliente tipo 2 "
                        nuevo_cliente = Persona(2)
                        self.inmobiliaria.atender(nuevo_cliente, self.resultados, self.tiempo_simulacion)
                    elif value <= 0.927:
                        text += "Cliente tipo 3 "
                        nuevo_cliente = Persona(3)
                        self.inmobiliaria.atender(nuevo_cliente, self.resultados, self.tiempo_simulacion)
                    else:
                        text += "Cliente tipo 4 "
                        nuevo_cliente = Persona(4)
                        self.inmobiliaria.atender(nuevo_cliente, self.resultados, self.tiempo_simulacion)
            self.tiempo_simulacion += 1
        """print("[CLIENTES ATENDIDOS]: tipo 1: {}, tipo 2: {}, tipo 3: {},"
              " tipo 4: {}, total: {}".format(len(self.tiempos_llegada_clientes1),
              len(self.tiempos_llegada_clientes2), len(self.tiempos_llegada_clientes3),
              len(self.tiempos_llegada_clientes4), len(self.tiempos_llegada_clientes)))
        print("[CLIENTES 1 COMPRARON]: 0")
        print("[CLIENTES 2 COMPRARON]: 0")
        print("[CLIENTES 3 COMPRARON]: 0")
        print("[CLIENTES 4 COMPRARON]: 0")
        print("[CLIENTES PERDIDOS]: {}".format(len(self.tiempos_llegada_clientes) - 0))"""
        casas_vendidas = 0
        ingresos = 0
        for i in self.inmobiliaria.casas:
            if i.vendida:
                casas_vendidas += 1
                ingresos += i.precio
        print("[CASAS VENDIDAS]: {}".format(casas_vendidas))
        print("[INGRESOS]: ${}".format(ingresos))

        
        #Guardar los resultados en el excel
        self.resultados.fin_simulacion()
        return casas_vendidas, ingresos


if __name__ == '__main__':
    cantidad_simulaciones = 100

    """En este ejemplo inicializamos la simulacion en 2 semanas, o 336 horas como tiempo maximo."""
    maximo_tiempo = 16800


    """Tasas de llegada de los clientes
    Asumiendo meses de 30 dias y una tasa de 140 clientes por mes
    la tasa queda como 140 / 720"""
    tasa_llegada_clientes = 20 / 720
    
    semanas_cambio = [7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47, 51,
              55, 59, 63, 67, 71, 75, 79, 83, 87, 91, 95, 99]

    def grades_variance(scores):
        average = sum(scores)/len(scores)
        sumatorio = 0
        for data in scores:
            sumatorio += (average - float(data)) ** 2
        variance = float(sumatorio) / len(scores)
        return variance
    '''En este punto utilizamos la información de todas las simulaciones para generar los excels con
    la información útil en el análisis de resultados'''
    ingresos_primera_fijacion = []
    casas_vendidas_primera_fijacion = []
    matriz_de_precios_casas_vendidas = [] # lista de listas de tuplas
    lista_cantidad_personas_no_compran = []
    matriz_factor_precios_para_cada_casa_por_periodo = []
    matriz_precios_para_cada_casa_por_periodo = []
    for i in range(cantidad_simulaciones):
        print("simulacion " + str(i))
        s = Simulacion(maximo_tiempo, tasa_llegada_clientes,
                       alfa=3.3, coef=7, no_compra=1.2, cambio=semanas_cambio,
                       tolerancia_cambio=0.54)
        casas, ingresos = s.run()
        ingresos_primera_fijacion.append(ingresos)
        casas_vendidas_primera_fijacion.append(casas)
        matriz_de_precios_casas_vendidas.append(s.inmobiliaria.precios_casas_vendidas)
        lista_cantidad_personas_no_compran.append(s.inmobiliaria.cantidad_personas_no_compran)
        matriz_factor_precios_para_cada_casa_por_periodo.append(s.inmobiliaria.factor_precios_por_casa_para_cada_periodo)
        matriz_precios_para_cada_casa_por_periodo.append(s.inmobiliaria.precios_por_casa_para_cada_periodo)
    print("-"*20+"RESULTADOS"+"-"*20)
    print("Ingresos promedio primera fijacion: {}, varianza: "
          "{}".format(sum(ingresos_primera_fijacion)/len(ingresos_primera_fijacion)
                      ,grades_variance(ingresos_primera_fijacion)))
    print("Casas vendidas promedio primera fijacion: {}, varianza: "
              "{}".format(sum(casas_vendidas_primera_fijacion)/len(casas_vendidas_primera_fijacion)
                          ,grades_variance(casas_vendidas_primera_fijacion)))
    print(matriz_de_precios_casas_vendidas)
    precios_promedio_casas_vendidas = []
    '''lista de listas, indice de lista + 1 es la casa, primera pos tupla precio promedio, segunda posicion varianza'''
    for i in range(0, 100):
        lista_precios_casa_id = []
        for lista_tuplas in matriz_de_precios_casas_vendidas:
            for tupla in lista_tuplas:
                if tupla[0] == "Casa "+str(i + 1):
                    lista_precios_casa_id.append(tupla[1])
                    break
        try:
            promedio = sum(lista_precios_casa_id)/len(lista_precios_casa_id)
            varianza = grades_variance(lista_precios_casa_id)
        except ZeroDivisionError:
            promedio = 'casa no vendida nunca'
            varianza = 0
        precios_promedio_casas_vendidas.append((promedio, varianza))

    docu = Docu2(precios_promedio_casas_vendidas)
    docu.cantidad_personas_no_compra(lista_cantidad_personas_no_compran,
                                     grades_variance(lista_cantidad_personas_no_compran), cantidad_simulaciones)
    docu.cantidad_personas_compra(casas_vendidas_primera_fijacion, grades_variance(casas_vendidas_primera_fijacion),
                                  cantidad_simulaciones)
    factor_precio_promedio_y_varianza_por_casa_y_periodo = []
    '''lista de listas, primer index de lista + 1 indica la casa, segundo index indica el periodo de cambio de precio,
     el contenido de factor_precio[i][j] es una tupla, en primera posición está factor precio promedio,
     en segunda posición su varianza'''
    for casa in range(100):
        lista_factores_periodo_una_casa = []
        for periodo in range(25):
            lista_factores_precio = []
            for sim in range(cantidad_simulaciones):
                lista_factores_precio.append(
                    matriz_factor_precios_para_cada_casa_por_periodo[sim][casa][periodo])
            lista_factores_periodo_una_casa.append((sum(lista_factores_precio)/len(lista_factores_precio),
                                                    grades_variance(lista_factores_precio)))
        factor_precio_promedio_y_varianza_por_casa_y_periodo.append(lista_factores_periodo_una_casa)
    docu.factor_precios_por_periodo(factor_precio_promedio_y_varianza_por_casa_y_periodo)



    precio_promedio_y_varianza_por_casa_y_periodo = []
    '''lista de listas, primer index de lista + 1 indica la casa, segundo index indica el periodo de cambio de precio,
     el contenido de factor_precio[i][j] es una tupla, en primera posición está precio promedio,
     en segunda posición su varianza'''
    for casa in range(100):
        lista_precio_periodo_una_casa = []
        for periodo in range(25):
            lista_precio = []
            for sim in range(cantidad_simulaciones):
                lista_precio.append(
                    matriz_precios_para_cada_casa_por_periodo[sim][casa][periodo])
            lista_precio_periodo_una_casa.append((sum(lista_precio)/len(lista_precio),
                                                    grades_variance(lista_precio)))
        precio_promedio_y_varianza_por_casa_y_periodo.append(lista_precio_periodo_una_casa)
    docu.precios_promedio_por_periodo(precio_promedio_y_varianza_por_casa_y_periodo)





'''Esta parte fue usada para el cálculo de los valores óptimos de alpha y tolerancia de cambio en la simulacion'''
#    alfas = [i/10 for i in range(25,40)]
#    tolerancias = [0.06 * i for i in range(10)]
#    tolerancias = [0.05, 0.3, 0.6]
#    ingresosl = []
#    casasl = []
#    resultados = [[], [], [], []]
#    for i in range(len(alfas)):
#        param_alfa = alfas[i]
#        
#        for j in range(len(tolerancias)):
#            param_tolerancia = tolerancias[j]
#            simus = []
#            for k in range(5):
#            
#                s = Simulacion(maximo_tiempo, tasa_llegada_clientes,
#                               alfa=param_alfa, coef=7, no_compra=1.2, cambio=semanas_cambio,
#                               tolerancia_cambio=param_tolerancia)
#                casas_vendidas, ingresos = s.run()
#                simus.append(ingresos)
#            resultados[0].append(param_alfa)
#            resultados[1].append(param_tolerancia)
#            resultados[2].append(np.mean(simus))
#            resultados[3].append(casas_vendidas)
#
#
#            print(casas_vendidas, ingresos)
#            print(param_alfa, param_tolerancia)
#    fig = plt.figure()
#    ax = fig.add_subplot(111, projection='3d')
#    
#    n = 100
#    
#    # For each set of style and range settings, plot n random points in the box
#    # defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
#    xs = resultados[0]
#    ys = resultados[1]
#    zs = resultados[2]
#    ax.scatter(xs, ys, zs)
#    
#    ax.set_xlabel('Fijacion Inicial')
#    ax.set_ylabel('Fijacion Dinamica')
#    ax.set_zlabel("Ingresos")
#    
#    plt.show()
