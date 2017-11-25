# -*- coding: utf-8 -*-
"""
Created on ??

@author: Luis
"""

from random import randint, expovariate, random
from cargar_modelo_comp import Prediccion_Preferencias
from logit import calculo_probs
from importar_datos import importar_casas
from documentar import Documentador


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


class Inmobiliaria:


    def __init__(self):
        self.nombre = "Inmobiliaria S.A"
        #Por ahora las casa se definen con precios random y los atributos del excel 
        precios_casas = [randint(100, 200) for i in range(100)]

        atributos = importar_casas()
        self.casas = []
        for i in range(0, 100):
            self.casas.append(Casa(atributos[i][0], atributos[i][1:15], precios_casas[i]))

            """ En caso que quisieramos poner los precios de las casa del excel
            habría que ocupar esta linea de codigo en vez de la anterior"""
            #self.casas.append(Casa(atributos[i][0], atributos[i][1:15], atributos[i][15]))


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
        utis, probs = calculo_probs(tuplas)

        """Asignamos a cada casa su correspondiente utlidad y 
        probabilidad de no compra"""
        for i in range(len(casas_disponibles)):
            casas_disponibles[i].utilidad = utis[i]
            casas_disponibles[i].probabilidad = probs[i]

        #Se ordenan las casas segun su utilidad de mayor a menor
        casas_disponibles = sorted(casas_disponibles, key=lambda x: x.utilidad, reverse=True)

        """Comprobamos con las primeras 5 (se puede cambiar) casas si alguna se vende"""
        for i in range(5):
            value = random()
            if casas_disponibles[i].probabilidad < value:
                casas_disponibles[i].vendida = True
                print("{} vendida".format(casas_disponibles[i].identificador))
                documentador.casa_vendida(casas_disponibles[i], tiempo)
                break


class Simulacion:


    def __init__(self, tiempo_maximo, tasa_llegada):
        self.tiempo_maximo_sim = tiempo_maximo
        self.tasa_llegada_clientes = tasa_llegada
        self.tiempo_simulacion = 1
        self.inmobiliaria = Inmobiliaria()
        self.clientes_tipo1_atendidos = 0
        self.clientes_tipo2_atendidos = 0
        self.clientes_tipo3_atendidos = 0
        self.clientes_tipo4_atendidos = 0
        self.clientes_perdidos = 0
        self.resultados = Documentador(self.inmobiliaria)

    def llegadas_clientes(self, tasa_llegada):
        tiempos_entre_llegada_clientes = [round(expovariate(tasa_llegada))]
        while sum(tiempos_entre_llegada_clientes) <= 336:
            tiempos_entre_llegada_clientes.append(round(expovariate(tasa_llegada)))
        tiempos_entre_llegada_clientes.pop()
        print("-" * 40 + "DEFINICION DE TIEMPOS" + "-" * 40)
        print("\n")
        print("TIEMPOS ENTRE LLEGADAS CLIENTES: {}, suma: {}".format(tiempos_entre_llegada_clientes,
                                                                      sum(tiempos_entre_llegada_clientes)))

        self.tiempos_llegada_clientes = [sum(tiempos_entre_llegada_clientes[:i]) for i in \
                                    range(len(tiempos_entre_llegada_clientes)+1)][1::]

        print("\n")
        print("TIEMPOS LLEGADA CLIENTES: {}".format(self.tiempos_llegada_clientes))

    def run(self):
        """Este metodo ejecuta la simulacion de la inmobiliaria
        se estima aleatoreamente la llegada de clientes"""
        self.llegadas_clientes(self.tasa_llegada_clientes)

        print("\n\n\n")
        print("-"*40+"INICIO SIMULACIÓN"+ "-"*40)
        print("\n")

        """Ejecutamos el ciclo verificando que el tiempo de simulacion no supere
        el tiempo maximo de simulacion"""
        while self.tiempo_simulacion <= self.tiempo_maximo_sim:
            """Verificamos si en el tiempo actual(día) de la simulación llega algún cliente"""
            if not(self.tiempo_simulacion in self.tiempos_llegada_clientes):
                print("[HORA {}]: No llegan clientes a la inmobiliaria".format(self.tiempo_simulacion))
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
                print(text)
            self.tiempo_simulacion += 1
        print("\n\n\n")
        print("-" * 40 + "INFORMACIÓN" + "-" * 40)
        print("\n")
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



if __name__ == '__main__':
    """Se definen los tipos de clientes y sus preferencias"""
    personas = []

    """En este ejemplo inicializamos la simulacion en 2 semanas, o 336 horas como tiempo maximo."""
    maximo_tiempo = 336


    """Tasas de llegada de los clientes
    Asumiendo meses de 30 dias y una tasa de 140 clientes por mes
    la tasa queda como 140 / 720"""
    tasa_llegada_clientes = 140 / 720

    s = Simulacion(maximo_tiempo, tasa_llegada_clientes)
    s.run()

