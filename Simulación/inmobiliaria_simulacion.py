# -*- coding: utf-8 -*-
"""
Created on ??

@author: Luis
"""

from random import random, expovariate
from .cargar_modelo_comp import Prediccion_Preferencias


predictor = Prediccion_Preferencias()


class Persona:


    def __init__(self, tipo):
        self.tipo = tipo
        self.determinar_preferencias()

    def determinar_preferencias(self):
        self.preferencias = predictor.entregar_preferencias(self.tipo-1)


class Casa:


    def __init__(self, atributos, precio):
        self.atributos = atributos
        self.precio = precio
        self._vendida = False

    @property
    def vendida(self):
        return self._vendida

    @vendida.setter
    def vendida(self, valor):
        self._vendida = True
        self.precio_venta = valor


class Inmobiliaria:


    def __init__(self):
        self.nombre = "Inmobiliaria S.A"
        self.precios_casas = [random.randint(100, 200) for i in range(100)]

    def atender(self, cliente):
        pass


class Simulacion:


    def __init__(self, tiempo_maximo, tasa_llegada1, tasa_llegada2, tasa_llegada3,
                 tasa_llegada4):
        self.tiempo_maximo_sim = tiempo_maximo
        self.tasa_llegada_cliente1 = tasa_llegada1
        self.tasa_llegada_cliente2 = tasa_llegada2
        self.tasa_llegada_cliente3 = tasa_llegada3
        self.tasa_llegada_cliente4 = tasa_llegada4
        self.tiempo_simulacion = 1
        #self.inmobiliaria = Inmobiliaria(tipos)
        self.clientes_tipo1_atendidos = 0
        self.clientes_tipo2_atendidos = 0
        self.clientes_tipo3_atendidos = 0
        self.clientes_tipo4_atendidos = 0

    def llegadas_clientes(self, tasa_llegada1, tasa_llegada2, tasa_llegada3, tasa_llegada4):
        tiempos_entre_llegada_clientes1 = [round(expovariate(tasa_llegada1))]
        tiempos_entre_llegada_clientes2 = [round(expovariate(tasa_llegada2))]
        tiempos_entre_llegada_clientes3 = [round(expovariate(tasa_llegada3))]
        tiempos_entre_llegada_clientes4 = [round(expovariate(tasa_llegada4))]
        while sum(tiempos_entre_llegada_clientes1) <= 336:
            tiempos_entre_llegada_clientes1.append(round(expovariate(tasa_llegada1)))
        while sum(tiempos_entre_llegada_clientes2) <= 336:
            tiempos_entre_llegada_clientes2.append(round(expovariate(tasa_llegada2)))
        while sum(tiempos_entre_llegada_clientes3) <= 336:
            tiempos_entre_llegada_clientes3.append(round(expovariate(tasa_llegada3)))
        while sum(tiempos_entre_llegada_clientes4) <= 336:
            tiempos_entre_llegada_clientes4.append(round(expovariate(tasa_llegada4)))
        tiempos_entre_llegada_clientes1.pop()
        tiempos_entre_llegada_clientes2.pop()
        tiempos_entre_llegada_clientes3.pop()
        tiempos_entre_llegada_clientes4.pop()
        print("-" * 40 + "DEFINICION DE TIEMPOS" + "-" * 40)
        print("\n")
        print("TIEMPOS ENTRE LLEGADAS CLIENTE 1: {}, suma: {}".format(tiempos_entre_llegada_clientes1,
                                                                      sum(tiempos_entre_llegada_clientes1)))
        print("TIEMPOS ENTRE LLEGADAS CLIENTE 2: {}, suma: {}".format(tiempos_entre_llegada_clientes2,
                                                                      sum(tiempos_entre_llegada_clientes2)))
        print("TIEMPOS ENTRE LLEGADAS CLIENTE 3: {}, suma: {}".format(tiempos_entre_llegada_clientes3,
                                                                      sum(tiempos_entre_llegada_clientes3)))
        print("TIEMPOS ENTRE LLEGADAS CLIENTE 4: {}, suma: {}".format(tiempos_entre_llegada_clientes4,
                                                                      sum(tiempos_entre_llegada_clientes4)))


        self.tiempos_llegada_clientes1 = [sum(tiempos_entre_llegada_clientes1[:i]) for i in \
                                    range(len(tiempos_entre_llegada_clientes1)+1)][1::]
        self.tiempos_llegada_clientes2 = [sum(tiempos_entre_llegada_clientes2[:i]) for i in \
                                    range(len(tiempos_entre_llegada_clientes2)+1)][1::]
        self.tiempos_llegada_clientes3 = [sum(tiempos_entre_llegada_clientes3[:i]) for i in \
                                    range(len(tiempos_entre_llegada_clientes3)+1)][1::]
        self.tiempos_llegada_clientes4 = [sum(tiempos_entre_llegada_clientes4[:i]) for i in \
                                    range(len(tiempos_entre_llegada_clientes4)+1)][1::]

        print("\n")
        print("TIEMPOS LLEGADA CLIENTE 1: {}".format(self.tiempos_llegada_clientes1))
        print("TIEMPOS LLEGADA CLIENTE 2: {}".format(self.tiempos_llegada_clientes2))
        print("TIEMPOS LLEGADA CLIENTE 3: {}".format(self.tiempos_llegada_clientes3))
        print("TIEMPOS LLEGADA CLIENTE 4: {}".format(self.tiempos_llegada_clientes4))

        self.tiempos_llegada_clientes = sorted(self.tiempos_llegada_clientes1 +
                                                  self.tiempos_llegada_clientes2 +
                                                  self.tiempos_llegada_clientes3 +
                                                  self.tiempos_llegada_clientes4)
        print("\n")
        print("TIEMPOS LLEGADA CLIENTES: {}".format(self.tiempos_llegada_clientes))

    def run(self):
        """Este metodo ejecuta la simulacion de la inmobiliaria
        se estima aleatoreamente la llegada de clientes"""
        self.llegadas_clientes(self.tasa_llegada_cliente1, self.tasa_llegada_cliente2,
                               self.tasa_llegada_cliente3, self.tasa_llegada_cliente4)

        print("\n\n\n")
        print("-"*40+"INICIO SIMULACIÓN"+ "-"*40)
        print("\n")

        """Ejecutamos el ciclo verificando que el tiempo de simulacion no supere
        el tiempo maximo de simulacion"""
        while self.tiempo_simulacion <= self.tiempo_maximo_sim:
            """Verificamos si en el tiempo actual(día) de la simulación llega algún cliente"""
            if not(self.tiempo_simulacion in self.tiempos_llegada_clientes):
                print("[DIA {}]: No llegan clientes a la inmobiliaria".format(self.tiempo_simulacion))
            else:
                text = "[DIA {}]: Llega(n) ".format(self.tiempo_simulacion)
                if self.tiempo_simulacion in self.tiempos_llegada_clientes1:
                    text += "{} cliente(s) tipo 1 ".format(self.tiempos_llegada_clientes1.count(self.tiempo_simulacion))
                    for i in range(self.tiempos_llegada_clientes1.count(self.tiempo_simulacion)):
                        nuevo_cliente = Persona(1)
                        """Acá hay que simular una atención de la inmobiliaria"""

                if self.tiempo_simulacion in self.tiempos_llegada_clientes2:
                    text += "{} cliente(s) tipo 2 ".format(self.tiempos_llegada_clientes2.count(self.tiempo_simulacion))
                    for i in range(self.tiempos_llegada_clientes2.count(self.tiempo_simulacion)):
                        nuevo_cliente = Persona(2)
                        """Acá hay que simular una atención de la inmobiliaria"""
                if self.tiempo_simulacion in self.tiempos_llegada_clientes3:
                    text += "{} cliente(s) tipo 3 ".format(self.tiempos_llegada_clientes3.count(self.tiempo_simulacion))
                    for i in range(self.tiempos_llegada_clientes3.count(self.tiempo_simulacion)):
                        nuevo_cliente = Persona(3)
                        """Acá hay que simular una atención de la inmobiliaria"""
                if self.tiempo_simulacion in self.tiempos_llegada_clientes4:
                    text += "{} cliente(s) tipo 4 ".format(self.tiempos_llegada_clientes4.count(self.tiempo_simulacion))
                    for i in range(self.tiempos_llegada_clientes4.count(self.tiempo_simulacion)):
                        nuevo_cliente = Persona(4)
                        """Acá hay que simular una atención de la inmobiliaria"""
                print(text)
            self.tiempo_simulacion += 1
        print("\n\n\n")
        print("-" * 40 + "INFORMACIÓN" + "-" * 40)
        print("\n")
        print("[CLIENTES ATENDIDOS]: tipo 1: {}, tipo 2: {}, tipo 3: {},"
              " tipo 4: {}, total: {}".format(len(self.tiempos_llegada_clientes1),
              len(self.tiempos_llegada_clientes2), len(self.tiempos_llegada_clientes3),
              len(self.tiempos_llegada_clientes4), len(self.tiempos_llegada_clientes)))
        print("[CLIENTES 1 COMPRARON]: 0")
        print("[CLIENTES 2 COMPRARON]: 0")
        print("[CLIENTES 3 COMPRARON]: 0")
        print("[CLIENTES 4 COMPRARON]: 0")
        print("[CLIENTES PERDIDOS]: {}".format(len(self.tiempos_llegada_clientes) - 0))
        print("[CASAS VENDIDAS]: 0")
        print("[INGRESOS]: $0")



if __name__ == '__main__':
    """Se definen los tipos de clientes y sus preferencias"""
    personas = []

    """En este ejemplo inicializamos la simulacion en 2 semanas, o 336 horas como tiempo maximo."""
    maximo_tiempo = 336

    """Definimos la tasa de llegada de los clientes en:
                                   1) un cliente tipo 1 cada 96 horas.
                                   2) un cliente tipo 2 cada 72 horas.
                                   3) un cliente tipo 3 cada 48 horas.
                                   4) un cliente tipo 4 cada 24 horas."""

    """Tasas de llegada de los clientes"""
    tasa_llegada_clientes1 = 1 / 96
    tasa_llegada_clientes2 = 1 / 72
    tasa_llegada_clientes3 = 1 / 48
    tasa_llegada_clientes4 = 1 / 24

    s = Simulacion(maximo_tiempo, tasa_llegada_clientes1, tasa_llegada_clientes2, tasa_llegada_clientes3,
                   tasa_llegada_clientes4)
    s.run()