#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Two functions to import data above a performance threshold:
    - one for numpy
    - one for pandas (more handy).
One function to generate caption for graphs.

@author: Lucie Wang
"""

import os
from utils import import_one_subject, get_serie_data
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

def import_good_enough_np(maxi = 15, exp_type = None):
    """
    Import data from subjects above a performance threshold.
    Input: maximal error rate accepted (in %), experiment type (1 for timing, 0 for motricity)
    Output: list (by subject) of dictionaries (by attribute) of lists (by trial).
    """
    ## Import all data
    data = [None] * 3  # data[session][subject] : data for given subject of a given session

    is_active = [None] * 3  # is_active[session][subject] : boolean whether a given subject of a given session counts in our data

    for session in range(3):
        data[session] = [None] * 20
        is_active[session] = [False] * 20

        rootdir = "../Data/Session " + str(session + 1)

        for file in os.listdir(rootdir):
            if file.endswith(".xpd"):
                subj = int(file.split("_")[1]) - 1
                data[session][subj] = import_one_subject(rootdir, file)
                is_active[session][subj] = True

    ## Get error rates
    err = [None] * 3
    for session in range(3):
        err[session] = [None] * 20
        for subj in range(20):
            if is_active[session][subj]:
                err[session][subj] = 1 - np.sum(data[session][subj]["Correct"]) / len(data[session][subj]["Correct"])

    # Import data only when error rate is below threshold
    filtered_data = []
    sessions = {None: [0, 1, 2], 0: [0], 1: [1, 2]}
    for session in sessions[exp_type]:
        for subj in range(20):
            if is_active[session][subj]:
                if err[session][subj] < maxi/100:
                    filtered_data.append(data[session][subj])

    return filtered_data

#dat = import_good_enough(30, 1)
#print(len(dat))

def import_good_enough_pd(maxi = 15, exp_type = None, dev = False):
    """
    Import data from subjects above a performance threshold.
    Input: maximal error rate accepted (in %), experiment type (1 for timing, 0 for motricity), developer mode
    Output: Panda dataframe (double-indexed by subject then trial).
    """
    l = []
    if dev:
        dat = [import_one_subject("../Data/Session 1", "firstexample_01_202001221414.xpd"), import_one_subject("../Data/Session 1", "firstexample_02_202001221414.xpd")]
    else:
        dat = import_good_enough_np(maxi, exp_type)
    N = len(dat) # number of subjects
    for subj in range(N):
        l.append(pd.DataFrame.from_dict(dat[subj]))
    return pd.concat(l, keys = [subj for subj in range(N)], names = ["subj"])


dat = import_good_enough_pd(25, dev = True)
print(len(dat.index.levels[0]))
print(len(dat.index.unique(0)))

def info_data(maxi = 15, exp_type = None):
    """
    Add caption in a pyplot graph, contains info about the data used.
    Input: maximal error rate accepted (in %), experiment type (1 for timing, 0 for motricity).
    """
    dat = import_good_enough_pd(maxi, exp_type)
    effectif = len(dat.index.unique(0))
    plt.figtext(0.5,0, "Statistique sur un total de {} sujets".format(effectif) + "\n" + ("Expérience 1 (timing)" if exp_type==1 else ("Expérience 2 (motricité)" if exp_type==0 else "Expériences 1 et 2")), verticalalignment='bottom', horizontalalignment='center')

