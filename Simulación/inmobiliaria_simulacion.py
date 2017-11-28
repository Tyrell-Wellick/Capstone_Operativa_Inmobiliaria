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
from numpy.random import choice
from numpy import cumsum


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
        self.precio_anterior = precio
        self.precio_inicial = precio
        self._vendida = False
        #Variable para la fijacion dinamica
        self.precio_minimo = 0
        #Estas variables sirven al momento de atender un cliente
        self.utilidad = 0
        self.probabilidad = 0
        #Variable para documentacion
        self.comprado_por = 0

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
        self.nombre = "Inmobiliaria S.A"
        #Por ahora las casa se definen con precios random y los atributos del excel 
#        precios_casas = [randint(180, 200) for i in range(100)]

        atributos = importar_casas(alfa)
        self.coef = coef
        self.no_compra = no_compra
        self.casas = []
        for i in range(0, 100):
#            self.casas.append(Casa(atributos[i][0], atributos[i][1:15], precios_casas[i]))

            """ En caso que quisieramos poner los precios de las casa del excel
            habría que ocupar esta linea de codigo en vez de la anterior"""
            self.casas.append(Casa(atributos[i][0], atributos[i][1:15], atributos[i][15]))


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
            #casas_disponibles[i].probabilidad = 1 - probs[i]
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
#        print(tuplas)
#        print(probs2)
#        draw = choice(casas_ofrecidas, 1, p=probs2)
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
            print("No compra")
        else:
            for c in range(len(casas_disponibles)):
                if casas_disponibles[c] == draw:
                    print("{} vendida a cliente tipo {}".format(casas_disponibles[c].identificador, cliente.tipo))
                    documentador.casa_vendida(casas_disponibles[c], tiempo, cliente.tipo)
                    casas_disponibles[c].vendida = True
                    #casas_disponibles.pop(c)
                    break

       # casas_disponibles.pop(draw)
        #if casas_disponibles[i].probabilidad < probs[i]:
        #    casas_disponibles[i].vendida = True
        #    print("{} vendida a cliente tipo {}".format(casas_disponibles[i].identificador, cliente.tipo))
        #    documentador.casa_vendida(casas_disponibles[i], tiempo, cliente.tipo)
           # break


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
        """Variable auxiliar para calcular precios"""
        self.nro_casas_antes = 100
        self.semana_period_anter = 0

    def llegadas_clientes(self, tasa_llegada):
        tiempos_entre_llegada_clientes = [round(expovariate(tasa_llegada))]
        while sum(tiempos_entre_llegada_clientes) <= self.tiempo_maximo_sim:
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
        
    def actualizar_precios(self, semana):
        semana = semana /(7*24)
        num_vendidas = len([i for i in self.inmobiliaria.casas if i.vendida])
        print(semana, 'se actualizan precios')
        factor = num_vendidas/semana
        print(factor, 'factor')
        if factor >= 1 + self.tolerancia_cambio:
            factor = 1 + self.tolerancia_cambio
            
        elif factor <= 1 - self.tolerancia_cambio:
            factor =  1 - self.tolerancia_cambio
        
        
        for casa in self.inmobiliaria.casas:
            if not casa.vendida:
                casa.cambiar_precio(factor)

    def actualizar_precios2(self, semana):
        semana = semana/(7*24)
        """Los dos primeros periodos deben tener precio constante"""
        if semana == 7:
            return None 
        """El numero esperado de casas que se esperaba vender era
        el numero de casas que restaban partido el numero de semanas
        que quedan de horizonte temporal"""
        esperado = len([i for i in self.inmobiliaria.casas if i.vendida]) / (100 - self.semana_period_anter)
        self.semana_period_anter = semana
        """Calculamos el numero de casas que se vendieron en el periodo
        y luego se reemplaza el valor de casa que quedan por el actual"""
        num_vendidas_periodo = self.nro_casas_antes - len([i for i in self.inmobiliaria.casas if i.vendida])
        self.nro_casas_antes = len([i for i in self.inmobiliaria.casas if i.vendida])
        """Iteramos sobre cada casa para calcular su valor"""
        for casa in self.inmobiliaria.casas:
            if not casa.vendida:
                if casa.precio_anterior > casa.precio: #Precio disminuyo
                    new_price = casa.precio + (casa.precio_anterior - casa.precio) * (num_vendidas_periodo - esperado)/esperado
                elif casa.precio_anterior < casa.precio: #Precio aumento
                    new_price = casa.precio - (casa.precio_anterior - casa.precio) * (num_vendidas_periodo - esperado)/esperado
                else: #Precio se mantuvo
                    new_price = casa.precio + casa.precio * (casa.precio / casa.precio_inicial) * (num_vendidas_periodo - esperado)/esperado
                """Si el nuevo precio excede el precio inicial, se fija
                este como tope"""
                if new_price > casa.precio_inicial:
                    new_price = casa.precio_inicial
                if new_price < casa.precio_minimo:
                    new_price = casa.precio_minimo
                casa.precio_anterior = casa.precio
                casa.precio = new_price

    def actualizar_precios3(self, semana):
        semana = semana/(7*24)
        """Los dos primeros periodos deben tener precio constante"""
        if semana == 7:
            return None 
        """El numero esperado de casas que se esperaba en total es
        igual al numero de semanas transcurridas"""
        esperado_total = semana
        """Calculamos el numero de casas que se vendieron en el periodo"""
        num_vendidas = len([i for i in self.inmobiliaria.casas if i.vendida])
        """Iteramos sobre cada casa para calcular su valor"""
        for casa in self.inmobiliaria.casas:
            if not casa.vendida:
                if casa.precio_anterior > casa.precio: #Precio disminuyo
                    new_price = casa.precio + (casa.precio_inicial - casa.precio) * (num_vendidas - esperado_total)/esperado_total
                else: #Precio se mantuvo
                    new_price = casa.precio + casa.precio * (casa.precio / casa.precio_inicial) * (num_vendidas - esperado_total)/esperado_total
                """Si el nuevo precio excede el precio inicial, se fija
                este como tope"""
                if new_price > casa.precio_inicial:
                    new_price = casa.precio_inicial
                if new_price < casa.precio_minimo:
                    new_price = casa.precio_minimo
                casa.precio_anterior = casa.precio
                casa.precio = new_price



    def run(self):
        """Este metodo ejecuta la simulacion de la inmobiliaria
        se estima aleatoreamente la llegada de clientes"""
        self.llegadas_clientes(self.tasa_llegada_clientes)
        self.resultados.cambio_precio(0)

        print("\n\n\n")
        print("-"*40+"INICIO SIMULACIÓN"+ "-"*40)
        print("\n")

        """Ejecutamos el ciclo verificando que el tiempo de simulacion no supere
        el tiempo maximo de simulacion"""
        while self.tiempo_simulacion <= self.tiempo_maximo_sim:
            """Verificamos si en el tiempo actual(día) de la simulación llega algún cliente"""
            if not(self.tiempo_simulacion in self.tiempos_llegada_clientes):
#                print("[HORA {}]: No llegan clientes a la inmobiliaria".format(self.tiempo_simulacion))
                pass
            if (self.tiempo_simulacion in self.t_cambios):
                """OJO! Dejar solo uno sin comentar, cada funcion corresponde
                a cada enfoque"""
                self.actualizar_precios(self.tiempo_simulacion)
                #self.actualizar_precios2(self.tiempo_simulacion)
                #self.actualizar_precios3(self.tiempo_simulacion)
                
                self.resultados.cambio_precio(self.tiempo_simulacion/(7*24))

            else:
                text = "[HORA {}]: Llega(n) ".format(self.tiempo_simulacion)
                for i in range(self.tiempos_llegada_clientes.count(self.tiempo_simulacion)):
                    value = random() #Con esto verificamos de que tipo es el cliente
                    if value <= 0.432:
                        text += "Cliente tipo 1 "
                        nuevo_cliente = Persona(1)
#                        print(text)
                        self.inmobiliaria.atender(nuevo_cliente, self.resultados, self.tiempo_simulacion)
                    elif value <= 0.724:
                        text += "Cliente tipo 2 "
                        nuevo_cliente = Persona(2)
#                        print(text)
                        self.inmobiliaria.atender(nuevo_cliente, self.resultados, self.tiempo_simulacion)
                    elif value <= 0.927:
                        text += "Cliente tipo 3 "
                        nuevo_cliente = Persona(3)
#                        print(text)
                        self.inmobiliaria.atender(nuevo_cliente, self.resultados, self.tiempo_simulacion)
                    else:
                        text += "Cliente tipo 4 "
                        nuevo_cliente = Persona(4)
#                        print(text)
                        self.inmobiliaria.atender(nuevo_cliente, self.resultados, self.tiempo_simulacion)

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
    maximo_tiempo = 16800


    """Tasas de llegada de los clientes
    Asumiendo meses de 30 dias y una tasa de 140 clientes por mes
    la tasa queda como 140 / 720"""
    tasa_llegada_clientes = 20 / 720
    
    semanas_cambio = [7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47, 51,
              55, 59, 63, 67, 71, 75, 79, 83, 87, 91, 95, 99]

    s = Simulacion(maximo_tiempo, tasa_llegada_clientes,
                   alfa=2, coef=5, no_compra=1.2, cambio=semanas_cambio,
                   tolerancia_cambio = 0.1)
    s.run()

