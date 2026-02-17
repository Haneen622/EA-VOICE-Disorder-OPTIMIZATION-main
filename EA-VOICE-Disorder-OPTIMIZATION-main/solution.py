# -*- coding: utf-8 -*-
"""
Created on Tue May 17 15:50:25 2016

@author: hossam
"""

import time
import numpy

class solution:
    def __init__(self):
        self.best = float("inf")
        self.bestIndividual = []
        self.convergence = []
        self.startTime = time.strftime("%Y-%m-%d-%H-%M-%S")
        self.endTime = None
        self.executionTime = None
        self.optimizer = None
        self.objfname = None
