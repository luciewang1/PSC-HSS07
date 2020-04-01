#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains function that will be used for data analysis
@author: Florent Meyniel
"""
import numpy as np
from expyriment.misc import data_preprocessing
from ComputeSurprise import add_surprise


def import_one_subject(rootdir, file_name, with_surprise = False):
    """
    Import the data of one subject, and do some basic preprocessing.
    """

    # Load data file
    agg = data_preprocessing.Aggregator(data_folder=rootdir, file_name=file_name)

    # ignore lines that correspond to the register of >2 presses per trial
    trial = agg.get_variable_data("TrialId").flatten()
    n = len(trial)
    ignore = []
    for line in range(n):
        if line > 0:
            if trial[line] == trial[line-1]:
                ignore.append(1)
            else:
                ignore.append(0)
        else:
            ignore.append(0)
    ignore = np.array(ignore)
    trial = np.array(list(map(int, trial)))[ignore == 0]

    multi_press = agg.get_variable_data("IsMultiKeyPress").flatten()
    multi_press = np.array([0 if e == 'False' else (1 if e == 'True' else -1) for e in multi_press])
    multi_press = multi_press[ignore == 0]

    RT = agg.get_variable_data("RT").flatten()
    RT = np.array([int(rt) if rt != 'None' else -1 for rt in RT]).astype('int64')
    RT = RT[ignore == 0]

    Correct = agg.get_variable_data("Correct").flatten()
    Correct = np.array([1 if c == 'True' else 0 for c in Correct])
    Correct = Correct[ignore == 0]

    onset = agg.get_variable_data("StimulusOnset").flatten()
    onset = onset[ignore == 0]

    block = agg.get_variable_data("BlockId").flatten()
    block = np.array(list(map(int, block)))[ignore == 0]

    seq = agg.get_variable_data("Stimulus").flatten()
    seq = np.array([1 if stim == 'True' else 0 for stim in seq])
    seq = seq[ignore == 0]

    serie = agg.get_variable_data("SerieId").flatten()
    serie = np.array(list(map(int, serie)))[ignore == 0]

    motor = agg.get_variable_data("Motricity").flatten()
    motor = np.array(list(map(int, motor)))[ignore == 0]

    ecc = agg.get_variable_data("Eccentricity").flatten().astype('int64')
    ecc = np.array(list(map(int, ecc)))[ignore == 0]

    delay = agg.get_variable_data("Delay").flatten()
    delay = np.array(list(map(int, delay)))[ignore == 0]

    rep = agg.get_variable_data("Repetition").flatten()
    rep = np.array([1 if r == 'True' else 0 for r in rep])
    rep = rep[ignore == 0]

    dat = {"trial": trial, "multi_press": multi_press, "RT": RT, "Correct": Correct,
            "onset": onset, "block": block, "seq": seq, "serie": serie, "motor": motor, "ecc": ecc,
            "delay": delay, "rep" : rep}

    if with_surprise:
        return add_surprise(dat)

    return dat
#print(import_one_subject("../Data/Session 1", "firstexample_01_202001221414.xpd", with_surprise=True))

def get_serie_data(dat, varname, num_block, num_serie=None):
    """Get the variable *varname* from dat, for the specified block (and optionnaly, serie)"""

    if num_serie is None:
        ind = dat['block'] == num_block

    else:
        ind = (dat['block'] == num_block) & (dat['serie'] == num_serie)
    return dat[varname][ind]