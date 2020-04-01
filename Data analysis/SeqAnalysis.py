#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to quickly analyze the reaction time depending on past stimuli.
    - import data
    - compute the median RT / error rate depending on preceding sequences.
    - plot the corresponding graphs.
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
exp_type = 0 # 1 for delay, 0 for motricity, None for both
factors = ['ecc', 'motor', 'delay'] # list of factors to be distinguished (among 'ecc', 'motor', 'delay')
is_RT = True # True for RT, False for error rates

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

if is_RT:
    correct_df = df[df['Correct'] == True]
    partial_df = correct_df[factors + ['HistoryId', 'RT']]
    perf_df = partial_df.groupby(factors + ['HistoryId']).median()
    exploitable_df = perf_df.reset_index(level='HistoryId')
else:
    partial_df = df[factors + ['HistoryId', 'Correct']]
    print(partial_df)
    perf_df = partial_df.groupby(factors + ['HistoryId']).mean()
    print(perf_df)
    perf_df['Correct'] = perf_df['Correct'].map(lambda x: 100*(1-x)) # conversion to error rate (in %)
    print(perf_df)
    exploitable_df = perf_df.reset_index(level='HistoryId')
    print(exploitable_df)

## Plot graphs

conditions = {}
var = 'RT' if is_RT else 'Correct'

for i in exploitable_df.index.unique(): # different graphs
    print(i)
    conditions[i] = {'x' : [], 'y' : []}
for i, row in exploitable_df.iterrows(): # data for each graph
    conditions[i]['x'].append(row['HistoryId'])
    conditions[i]['y'].append(row[var])

for i in conditions:
    plt.plot(conditions[i]['x'], conditions[i]['y'], "o-", label = "{} : {}".format(str(exploitable_df.index.names), str(i)))

plt.xticks([n for n in range(16)], [str_of_seq(seq_of_int(n, k)) for n in range(N)], rotation=60, fontsize='small')
plt.ylabel("Reaction time (ms)" if is_RT else "Error rate (%)")
plt.title("{} depending on {} last stimuli".format("Reaction time" if is_RT else "Error rate", k))
plt.legend()

info_data(maxi, exp_type)

plt.show()