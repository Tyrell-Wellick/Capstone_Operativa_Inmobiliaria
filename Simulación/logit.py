# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 16:54:39 2017

@author: Nicolás
"""

import numpy as np
from functools import reduce


def calculo_probs(lista, coef, no_compra):
    utis = [((i[0])/i[1])**coef for i in lista]
    utis.append(no_compra**coef)
    expos = [np.exp(i) for i in utis]
    suma = reduce((lambda x, y: x + y), expos)
    probs = [i/suma for i in expos]
    return utis, probs