#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to quickly analyze the timing of stimuli in a dataset.
    - plot the histogram of stimulus onset asynchrony (SOA)
    - plot SOA, difference with expected timing of event and subject response

@author: Florent Meyniel
"""

from utils import import_one_subject, get_serie_data
import numpy as np
import matplotlib.pyplot as plt

# Get data (indicate path and file name of the dataset)
# rootdir = "../data"
# file_name = "florentm_01_20200112_speed.xpd"
# file_name = "florentm_02_20200112_lateralization.xpd"
rootdir = "../data/MSE15012020"
file_name = "firstexample_07_202001151523.xpd"

dat = import_one_subject(rootdir, file_name)


def shorter_name(string):
    """return a shorter version of the file name for display"""
    string = "".join(string.split('_')[1:])
    return string.split(".")[0]

# %% Histrogram of Stimulus onset asynchrony (SOA)

# Initialize
SOA = {}
for delay in np.unique(dat['delay']):
    SOA[delay] = []

# Get SOA in every series presented to subject
for block_num in np.unique(dat['block']):
    for serie_id in np.unique(get_serie_data(dat, 'serie', block_num)):
        delay = np.unique(get_serie_data(dat, 'delay', block_num, serie_id))[0]
        SOA[delay] += list(np.diff(get_serie_data(dat, 'onset', block_num, serie_id)))

# Plot SOA for the different delay conditions
for k in range(len(SOA)):
    plt.subplot(1, 2, 1+k)
    plt.hist(SOA[list(SOA.keys())[k]])
plt.title(f"{shorter_name(file_name)}: {int(np.mean(dat['RT'] != -1)*100)}% resp, " +
          f"{int(np.mean(dat['multi_press'] == 1)*100)}% multi")
plt.show()


# %% Plot SOA, shift w.r.t. predefined timings and reponses in one serie

# Set block and serie to display
block_num = 2.0
serie_id = 0.0

if block_num in set(dat['block']):
    if serie_id in set(get_serie_data(dat, 'serie', block_num)):

        # get SOA for this session
        onset = get_serie_data(dat, 'onset', block_num, serie_id)
        SOA = np.array([900] + list(np.diff(onset)))
        RT = get_serie_data(dat, 'RT', block_num, serie_id)
        multi_press = get_serie_data(dat, 'multi_press', block_num, serie_id)

        # Get expected interval between event on->off and off->on
        delays = [700, 1200]
        display_time = 200
        block_lengths = [25, 240]
        temps_rouge = [0]*(1+block_lengths[1])
        temps_bleu = [0]*(1+block_lengths[1])
        t_b, t_r = 0, 0
        for i in range(1, 1+block_lengths[1]):
            if i%2 == 1:
                t_b += display_time
                t_r += display_time
            else:
                t_b += delays[1]
                t_r += delays[0]
            temps_bleu[i], temps_rouge[i] = t_b, t_r
        temps = [temps_rouge, temps_bleu]
        time = temps[0] if get_serie_data(dat, 'delay', block_num, serie_id)[0] == 0.0 else temps[1]

        # Get expected onset
        expected_onset = time[0::2]
        expected_onset = expected_onset[:-1]

        # realign actual onset time on the first onset
        ronset = [val-onset[0] for val in onset]

        # Measure difference between expected and actual timing
        delta = np.array(ronset) - np.array(expected_onset)

        # Plot
        plt.plot([time[2]]*len(SOA), 'k', label='target')
        plt.plot(delta, '.-', label='delta')
        plt.plot(SOA, '.-', label='SOA')
        plt.plot([k for k in range(len(RT)) if RT[k] != -1],
                 [0 for k in range(len(RT)) if RT[k] != -1], '.', label='resp.')
        plt.plot([k for k in range(len(RT)) if RT[k] == -1],
                 [-50 for k in range(len(RT)) if RT[k] == -1], 'x', label='no resp.')
        plt.plot([k for k in range(len(RT)) if multi_press[k] == 1],
                 [-100 for k in range(len(RT)) if multi_press[k] == 1], '.', label='multi resp.')
    else:
        print('No such serie')
else:
    print('No such block')
plt.legend()


