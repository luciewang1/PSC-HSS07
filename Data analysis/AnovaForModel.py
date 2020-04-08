#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Perform Anova on RT regressed on some of the variables in X, in order to measure their actual impact.
"""

from FilterData import import_good_enough_pd#, info_data
import numpy as np
import pandas as pd
from statsmodels.stats.anova import AnovaRM
from statsmodels.formula.api import ols

# Set parameters

vars = ["center", "rep_center", "rep_later", "surprise"]
X_vars = ["block", "serie", "trial", "seq", "post-correct"]
n = 5
with_X = True
decay = 10

maxi = 15
exp_type = None

# Import and complete data

df = import_good_enough_pd(maxi, exp_type, with_surprise=True, decay=decay)
#print(df)

df["post-correct"] = df["Correct"].copy() # column for whether preceding answer was correct (1/0)
df["post-correct"] = df["post-correct"].shift(1)

df["rep_center"] = df["rep"].mul(df["ecc"] == 0) # column for repetition * 1_{ecc = 0}
df["rep_later"] = df["rep"].mul(df["ecc"] > 0) # column for repetition * 1_{ecc > 0}
df["center"] = (df["ecc"] == 0).astype(int) # column for whether ecc = 0
df = df.reset_index(level=["subj"])

# Clean up data

df = df[df['Correct'] == True]
df = df[df['trial'] > 0]
#df.dropna(subset=['surprise', "post-correct"], inplace=True)  # drop first trials of series

#print("----------final df----------")
#print(list(df.columns))
#print(df[['subj', 'trial', 'ecc', 'rep', 'rep_center', 'rep_later', 'center', 'Correct', 'post-correct']].iloc[240:600])
#print(df["post-correct"].unique())

# Perform Anova on RT

results = AnovaRM(df, depvar='RT', subject='subj', within=["block", "serie"], aggregate_func="mean").fit()
#print(results)

# Perform regression on RT depending on trial number

results = ols('RT ~ np.log(trial)', data=df).fit()
print(results.summary())
