# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 14:35:01 2017

@author: Nicolás
"""

import pickle
import numpy as np


class Prediccion_Preferencias:


    def __init__(self):
        """ con picke cargamos los archivos del modelo y la base de datos"""
        self.modelo = pickle.load(open('mejor_modelo.sav', 'rb'))
        self.X_train = pickle.load(open('X_train.sav', 'rb'))
        self.y_train = pickle.load(open('y_train.sav', 'rb'))
        self.X_test = pickle.load(open('X_test.sav', 'rb'))
        self.y_test = pickle.load(open('y_test.sav', 'rb'))

        """
        test tiene los atributos de la casa y del cliente en una lista"""
        self.test = [0, 0, 0, 0, 0, 5, 1, 2, 1, 1, 0, 1, 1,
                8.132, 1.74, 6.24, 2.24, 1.60, 1.94, 1.65, 4.01, 1.64]
        print("Predicción: {}".format(self.modelo.predict([self.test])))  #muestra la prediccion


        self.centros = [[7.22222222, 1.66666667, 6.44444444, 1.44444444, 1.77777778,
                    1.77777778, 1.22222222, 3.11111111, 1.66666667, 124.51333333],
                   [8.08333333, 2.08333333, 7.66666667, 2.66666667, 1.58333333,
                    1.5,        2,          7.16666667, 1.66666667, 172.67416667],
                   [8.25925926, 1.7037037,  6.2962963,  2.22222222, 1.62962963,
                    1.96296296, 1.66666667, 4.07407407, 1.7407407, 143.46851852],
                   [8.2,        1.76666667, 6.26666667, 2.13333333, 1.56666667,
                    1.9,        1.86666667, 6.76666667, 1.6,        158.24233333]]

        self.desvs = [[.971, .866, 1.666, .726, .833, .833, .44, 1.364, .866],
                 [.996, .9, 2.146, .492, .514, .797, 1.04, 1.585, .651],
                 [1.403, .868, 1.682, .847, .564, .897, .919, 1.685, .655],
                 [1.447, .678, 1.892, .819, .568, .758, 1.008, 1.194, .723]]

    def entregar_preferencias(self, tipo_cliente):
        atributos_cliente = [np.random.normal(self.centros[tipo_cliente][i],
                                              .1 * self.desvs[tipo_cliente][i]) for i
                             in range(len(self.centros[tipo_cliente]) - 1)]
        return atributos_cliente


