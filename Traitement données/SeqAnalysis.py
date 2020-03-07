#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to quickly analyze the reaction time depending on past stimuli.
    - import data
    - compute the median RT depending on preceding sequences.
    - plot the corresponding graph.
@author: Lucie Wang
"""

import os
from utils import import_one_subject, get_serie_data
from FilterData import import_good_enough_pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

## Set parameters

k = 4
exp_type = 1
maxi = 25

## Import all data

df = import_good_enough_pd(maxi, exp_type, dev = False)
N = df.shape[0] # number of rows


## Conversion functions

def int_of_seq(seq): # encode sequences of order k in range(2^k), by reverse binary reading
    k = len(seq)
    n = 0
    for i in range(k):
        n += seq[i]*(2**i)
    return n

def seq_of_int(n, k): # decode sequences of order k from range(2^k), by reverse binary writing
    num = n
    seq = [0]*k
    for i in range(k):
        if num%2:
            seq[i] = 1
        num //= 2
    return seq

def str_of_seq(seq): # write sequence as a string of A's and R's
    return ''.join(list(map(lambda x: 'R' if x else 'A', seq)))


## Add column for history

historyId = [None for ind in range(N)]
for ind in range(N):
    if df.iloc[ind]["trial"] >= k:
        historyId[ind] = int_of_seq([df.iloc[ind-k+i+1]["rep"] for i in range(k)])
df["HistoryId"] = historyId


## Plot histogram

for ecc in np.sort(df["ecc"].unique()):
    for mot in np.sort(df["motor"].unique()):
        for delay in np.sort(df["delay"].unique()):

            mask = (df["ecc"] == ecc) & (df["motor"] == mot) & (df["delay"] == delay) & df["Correct"]
            x = np.sort(df[mask]["HistoryId"].unique())
            y = []
            for histId in x:
                mask_hist = df["HistoryId"] == histId
                RT = df[mask & mask_hist]["RT"].median()
                y.append(RT)

            plt.plot(x, y, "o-", label = "ecc : %s, mot : %s, delay : %s" % (ecc, mot, delay))

plt.xticks(x, [str_of_seq(seq_of_int(i, k)) for i in range(N)], rotation=60, fontsize='small')
plt.ylabel("Reaction time (ms)")
plt.title("Reaction time depending on %s last stimuli" % (str(k)))
plt.legend()
plt.show()