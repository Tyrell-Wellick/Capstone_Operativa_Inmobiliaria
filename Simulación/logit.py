# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 16:54:39 2017

@author: Nicolás
"""

import numpy as np
from functools import reduce


#tuplas = [(0, 180), (120, 160), (100, 180), (100, 170), (220, 190)]
#



def calculo_probs(lista):
    coef = 20
    utis = [((i[0])/i[1])**coef for i in lista]
    utis.append(1)
    expos = [np.exp(i) for i in utis]
    suma = reduce((lambda x, y: x + y), expos)
    probs = [i/suma for i in expos]
    return utis, probs
#print(calculo_probs(a))
    