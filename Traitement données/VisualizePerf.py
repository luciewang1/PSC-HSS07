#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Basic visualization of the performance data.
    - plot the histogram of RTs
    - plot the histogram of error rates

@author: Lucie Wang
"""

import os
from utils import import_one_subject, get_serie_data
import numpy as np
import matplotlib.pyplot as plt

## Import all data

data = [None]*3 # data[session][subject] : data for given subject of a given session

is_active = [None]*3 # is_active[session][subject] : boolean whether a given subject of a given session counts in our data

for session in range(3):
    data[session] = [None]*20
    is_active[session] = [False]*20

    rootdir = "../Données/Session " + str(session+1)

    for file in os.listdir(rootdir):
        if file.endswith(".xpd"):
            subj = int(file.split("_")[1])-1
            data[session][subj] = import_one_subject(rootdir, file)
            is_active[session][subj] = True

## Compute median RT for each subject

agg_RT = []
RT = [None]*3
for session in range(3):
    RT[session] = [None]*20
    for subj in range(20):
        if is_active[session][subj]:
            RT[session][subj] = np.median(data[session][subj]["RT"])
            agg_RT.append(RT[session][subj])

## Compute error rate for each subject

agg_err = []
err = [None]*3
for session in range(3):
    err[session] = [None]*20
    for subj in range(20):
        if is_active[session][subj]:
            err[session][subj] = 1-np.sum(data[session][subj]["Correct"])/len(data[session][subj]["Correct"])
            agg_err.append(err[session][subj])

## Plot histogram

plt.subplot(2,1,1)
plt.hist(agg_RT)
plt.title("Histogramme des temps de réaction médians")

plt.subplot(2,1,2)
plt.hist(agg_err)
plt.title("Histogramme des taux d'erreur")
plt.show()