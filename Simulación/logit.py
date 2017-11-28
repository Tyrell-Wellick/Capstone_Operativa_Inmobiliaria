# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 16:54:39 2017

@author: Nicolás
"""

import numpy as np
from functools import reduce


#tuplas = [(0, 180), (120, 160), (100, 180), (100, 170), (220, 190)]
#

lala = [(152.35499334280863, 263.44627096774195), (152.35499334280863, 263.44627096774195),
 (152.35499334280863, 263.44627096774195),
 (152.35499334280863, 263.44627096774195), (154.99147759390073, 263.44627096774195)]

def calculo_probs(lista, coef, no_compra):
    utis = [((i[0])/i[1])**coef for i in lista]
    utis.append(no_compra**coef)
    expos = [np.exp(i) for i in utis]
    suma = reduce((lambda x, y: x + y), expos)
    probs = [i/suma for i in expos]
    return utis, probs


#for i in range(20):
#    print(calculo_probs(lala, i, 1.2))
#    print("\n")
#    