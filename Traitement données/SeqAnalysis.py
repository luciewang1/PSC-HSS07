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

## Helper functions

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

def int_of_str(s):
    if s == 'True':
        return 1
    return 0

## Compute median RT depending on sequence

def init(k, exp_type=None): # k : history order, exp_type = 0 (motricity) or 1 (timing)
    N = 2**k
    if exp_type == None: # RT[n] : list of RTs, for a given history sequence
        RT = [None]*N
        for n in range(N):
            RT[n] = []
        return RT
    else: # RT[ecc][param][n] : list of RTs, for given block parameters and a given history sequence
        RT = [None]*3
        for ecc in range(3):
            RT[ecc] = [None]*2
            for param in range(2):
                RT[ecc][param] = [None] * N
                for n in range(N):
                    RT[ecc][param][n] = []
        return RT

def add_subject(dat, RT, k, exp_type=None):
    for block_num in range(6):
        ecc = int(get_serie_data(dat, 'ecc', block_num)[0])
        if exp_type == 1:
            param = int(get_serie_data(dat, 'delay', block_num)[0])
        if exp_type == 0:
            param = int(get_serie_data(dat, 'motor', block_num)[0])
        for serie_id in range(2):
            serie_rep = get_serie_data(dat, 'rep', block_num, serie_id)
            serie_RT = get_serie_data(dat, 'RT', block_num, serie_id)
            for trial in range(k, len(serie_RT)):
                n = int_of_seq(list(map(int_of_str, serie_rep[trial - k + 1:trial + 1])))
                if serie_RT[trial] and serie_RT[trial] > 0: # cases excluded : RT = None
                    if exp_type == None:
                        RT[n].append(serie_RT[trial])
                    else:
                        RT[ecc][param][n].append(serie_RT[trial])
    return RT

def build_RT(k, exp_type=None): # RT[n] : median reaction time for a given sequence
    N = 2**k
    RT = init(k, exp_type)
    if exp_type == None:
        for session in range(3):
            for subj in range(20):
                if is_active[session][subj]:
                    RT = add_subject(data[session][subj], RT, k)
        for n in range(N):
            RT[n] = np.median(RT[n])
    else:
        for session in range(3):
            for subj in range(20):
                if is_active[session][subj]:
                    RT = add_subject(data[session][subj], RT, k, exp_type)
        for ecc in range(3):
            for param in range(2):
                for n in range(N):
                    RT[ecc][param][n] = np.median(RT[ecc][param][n]) if RT[ecc][param][n] else 0
    return RT

## Plot median RT depending on sequence

def plot_RT(k, exp_type=None):
    N = 2**k
    x = [i for i in range(N)]
    RT = build_RT(k, exp_type)
    if exp_type == None:
        plt.plot(x, RT, "o-")
    else:
        for ecc in range(3):
            for param in range(2):
                plt.plot(x, RT[ecc][param], "o-", label='ecc = ' + str(ecc) + ", " + ("delay" if exp_type else "mot") + " = " + str(param))
    plt.xticks(x, [str_of_seq(seq_of_int(i, k)) for i in range(N)], rotation=60, fontsize='small')
    plt.ylabel("Reaction time (ms)")
    plt.title("Reaction time depending on " + str(k) + " last stimuli" + (", in " + ("timing" if exp_type else "motricity") + " experiment" if exp_type != None else ""))
    plt.legend()
    plt.show()
plot_RT(4, exp_type=None)