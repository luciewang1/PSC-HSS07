#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Perform Anova on RT regressed on X variables, in order to see what to keep or not in X.
"""

from FilterData import import_good_enough_pd#, info_data
import numpy as np
import pandas as pd
from statsmodels.stats.anova import AnovaRM

# Set parameters

vars = ["center", "rep_center", "rep_later", "surprise"]
X_vars = ["block", "serie", "trial", "seq", "post-correct"]
n = 5
with_X = True
decay = 10
exp_type = None

# Import and complete data

def IORdf(maxi, exp_type, decay) :
    """ Return an IOR dataFrame
    Derived from IORdf function in Anova.py"""
    ## Import and clean data
    df = import_good_enough_pd(maxi, exp_type, with_surprise=True, decay=decay)
    correct_df = df[df['Correct'] == True]
    # Aggregate subject with their difference Median (RT_{Rep = 1}) - Median(RT_{Rep = 0})
    groups = correct_df.groupby(['subj','ecc','motor',"delay",'rep',"block","serie","trial","seq","Correct","surprise"])['RT']
    med = groups.quantile()
    DF = pd.DataFrame(med.diff())
    DF.reset_index(inplace= True)
    final = DF #final = DF[DF['rep']==1]
    final.rename(columns = {'RT' : 'IOR'}, inplace= True)
    #final.drop(columns = ['rep'], inplace = True)
    return final

df = IORdf(maxi=15, exp_type=None, decay=decay)
print(df)

df["post-correct"] = df["Correct"].copy() # column for whether preceding answer was correct (1/0)
df["post-correct"] = df["post-correct"].shift(1)

df["rep_center"] = df["rep"].mul(df["ecc"] == 0) # column for repetition * 1_{ecc = 0}
df["rep_later"] = df["rep"].mul(df["ecc"] > 0) # column for repetition * 1_{ecc > 0}
df["center"] = (df["ecc"] == 0).astype(int) # column for whether ecc = 0

df.dropna(subset=['surprise', "post-correct"], inplace=True)  # drop first trials of series

# Perform Anova on RT regressed on X

results = AnovaRM(df, depvar='IOR', subject='subj', within=["block", "serie", "trial"]).fit()
print(results)
