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
from FilterData import import_good_enough_np, info_data
import numpy as np
import matplotlib.pyplot as plt

## Import all data

exp_type = None

sessions = {None: [0, 1, 2], 0: [0], 1: [1, 2]}
data = [None]*3 # data[session][subject] : data for given subject of a given session
is_active = [None]*3 # is_active[session][subject] : boolean whether a given subject of a given session counts in our data

for session in range(3):
    data[session] = [None]*20
    is_active[session] = [False]*20

    rootdir = "../Data/Session " + str(session+1)

    for file in os.listdir(rootdir):
        if file.endswith(".xpd"):
            subj = int(file.split("_")[1])-1
            data[session][subj] = import_one_subject(rootdir, file)
            is_active[session][subj] = True

## Compute median RT for each subject

agg_RT = []
RT = [None]*3
for session in sessions[exp_type]:
    RT[session] = [None]*20
    for subj in range(20):
        if is_active[session][subj]:
            RT[session][subj] = np.median(data[session][subj]["RT"])
            agg_RT.append(RT[session][subj])

## Compute error rate for each subject

agg_err = []
err = [None]*3
for session in sessions[exp_type]:
    err[session] = [None]*20
    for subj in range(20):
        if is_active[session][subj]:
            err[session][subj] = 1-np.sum(data[session][subj]["Correct"])/len(data[session][subj]["Correct"])
            agg_err.append(err[session][subj])

## Plot histogram

fig = plt.figure()
info_data()
#plt.figtext(0.5,0, "Statistique sur un total de 56 sujets (18 expérience 1 + 38 expérience 2)", verticalalignment='bottom', horizontalalignment='center')

ax1 = fig.add_subplot(211)
ax1.hist(agg_RT, bins=10, rwidth=.95)
ax1.set_title("Histogramme des temps de réaction médians")

ax2 = fig.add_subplot(212)
ax2.hist(agg_err, bins=20, rwidth=.95)
ax2.set_title("Histogramme des taux d'erreur")

plt.show()
