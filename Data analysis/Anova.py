#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Conduct analysis of variance (ANOVA).
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
import scipy.stats as stats
#import researchpy as rp
import statsmodels.api as sm
from statsmodels.formula.api import ols

## Set parameters

maxi = 15
exp_type = None # 1 for delay, 0 for motricity, None for both

## Import and clean data

df = import_good_enough_pd(maxi, exp_type)
correct_df = df[df['Correct'] == True]

## Analyze variance

print(stats.f_oneway(correct_df['RT'][correct_df['ecc'] == 0], correct_df['RT'][correct_df['ecc'] == 1], correct_df['RT'][correct_df['ecc'] == 2]))
