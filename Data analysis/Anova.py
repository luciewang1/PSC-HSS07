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
import researchpy as rp
from statsmodels.formula.api import ols
from statsmodels.stats.anova import AnovaRM

def IORdf(maxi, exp_type) :
    """ Return an IOR dataFrame"""
    ## Import and clean data
    df = import_good_enough_pd(maxi, exp_type)
    correct_df = df[df['Correct'] == True]
    # Aggregate subject with their difference Median (RT_{Rep = 1}) - Median(RT_{Rep = 0})
    groups = correct_df.groupby(['subj','ecc','motor','rep'])['RT'] if exp_type == 0 else correct_df.groupby(['subj','ecc','delay','rep'])['RT']
    med = groups.quantile()
    DF = pd.DataFrame(med.diff())
    DF.reset_index(inplace= True)
    final = DF[DF['rep']==1]
    final.rename(columns = {'RT' : 'IOR'}, inplace= True)
    final.drop(columns = ['rep'], inplace = True)
    return final

# Perform Anova Analysis - exp_typ = 0 (Motor)
m = IORdf(maxi=15, exp_type=0)
results = AnovaRM( m, depvar='IOR', subject='subj', within=['ecc', 'motor']).fit()
print(results)

    # Perform Anova Analysis when the centered condition is excluded
m_decentered = m[m['ecc'] != 0]
results = AnovaRM( m_decentered, depvar='IOR', subject='subj', within=['ecc', 'motor']).fit()
print(results)

#Perform Anova Analysis - exp_typ = 1 (Delay)
d = IORdf(maxi=15,exp_type=1)
results = AnovaRM(d, depvar='IOR', subject='subj', within=['ecc', 'delay']).fit()
print(results)

    #Perform Anova analysis when the centered condition is excluded
d_decentered = d[d['ecc'] != 0]
results = AnovaRM(d_decentered, depvar='IOR', subject='subj', within=['ecc', 'delay']).fit()
print(results)

# Analysis : how factors influence mean(RT) ? Motor-type experience
alld = import_good_enough_pd(15, 0)
correct_alld = alld[alld['Correct'] == True]
correct_alld.reset_index(inplace=True)
results = AnovaRM(correct_alld, depvar = 'RT', subject='subj', within=['ecc','motor'], aggregate_func='mean').fit()
print(results)

# Analysis : how factors influence mean(RT) ? Delay-type experience
alld = import_good_enough_pd(15, 1)
correct_alld = alld[alld['Correct'] == True]
correct_alld.reset_index(inplace=True)
results = AnovaRM(correct_alld, depvar = 'RT', subject='subj', within=['ecc','delay'], aggregate_func='mean').fit()
print(results)





