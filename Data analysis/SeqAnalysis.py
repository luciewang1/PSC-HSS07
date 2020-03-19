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
from FilterData import import_good_enough_pd, info_data
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


## Set parameters

k = 4 # order of history
maxi = 15
exp_type = 0 # 1 for delay, 0 for motricity
factors = ['ecc', 'motor'] # list of factors to be distinguished (among 'ecc', 'motor', 'delay')


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


## Import all data

df = import_good_enough_pd(maxi, exp_type)
N = df.shape[0] # number of rows


## Operate on dataframe

historyId = [None for ind in range(N)] # add history column
for ind in range(N):
    if df.iloc[ind]["trial"] >= k:
        historyId[ind] = int_of_seq([df.iloc[ind-k+i+1]["rep"] for i in range(k)])
df["HistoryId"] = historyId

print(df)
correct_df = df[df['Correct'] == True]
print(correct_df)
partial_df = correct_df[factors + ['HistoryId', 'RT']]
print(partial_df)
perf_df = partial_df.groupby(factors + ['HistoryId']).median()
print(perf_df)
exploitable_df = perf_df.reset_index(level='HistoryId')
print(exploitable_df)

## Plot graphs

conditions = {}

for i in exploitable_df.index.unique(): # different graphs
    print(i)
    conditions[i] = {'x' : [], 'RT' : []}
for i, row in exploitable_df.iterrows(): # data for each graph
    conditions[i]['x'].append(row['HistoryId'])
    conditions[i]['RT'].append(row['RT'])

for i in conditions:
    plt.plot(conditions[i]['x'], conditions[i]['RT'], "o-", label = "{} : {}".format(str(exploitable_df.index.names), str(i)))

plt.xticks([n for n in range(16)], [str_of_seq(seq_of_int(n, k)) for n in range(N)], rotation=60, fontsize='small')
plt.ylabel("Reaction time (ms)")
plt.title("Reaction time depending on %s last stimuli" % (str(k)))
plt.legend()

info_data(maxi, exp_type)

plt.show()