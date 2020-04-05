#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fit models to experimental data, by cross-validation over all subjects (sci-kit learn library).
"""

#import os
from utils import import_one_subject, get_serie_data
from FilterData import import_good_enough_pd#, info_data
import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
#import scipy.stats as stats
#import researchpy as rp
#import statsmodels.api as sm
#from statsmodels.formula.api import ols
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.utils import shuffle

# Set parameters

vars = ["center", "rep_center", "rep_later", "surprise"]
X_vars = ["block", "serie", "trial", "seq", "post-correct"]
n = 5
with_X = True
decay = 10
exp_type = None

# Import and complete data

df = import_good_enough_pd(exp_type=exp_type, with_surprise=True, decay=decay) # whole dataframe

df["post-correct"] = df["Correct"].copy() # column for whether preceding answer was correct (1/0)
df["post-correct"] = df["post-correct"].shift(1)

df["rep_center"] = df["rep"].mul(df["ecc"] == 0) # column for repetition * 1_{ecc = 0}
df["rep_later"] = df["rep"].mul(df["ecc"] > 0) # column for repetition * 1_{ecc > 0}
df["center"] = (df["ecc"] == 0).astype(int) # column for whether ecc = 0

# Clean up and split data

df = df[df['Correct'] == True]  # correct trials only
df.dropna(subset=['surprise', "post-correct"], inplace=True)  # drop first trials of series

dats = []  # list of individual dataframes
for subj_id in df.index.unique(0):
    dats.append(df.loc[subj_id])

# Compute cross-validation scores

def cross_val(vars, n=5, with_X=True):
    """
    Cross-validate a linear model over all subjects, by aggregating scores obtained individually.
    Input: list of regressor variables (strings), number of folds for n-fold cross-validation, base regressors X (True if to be included).
    Output: array of cross-validation scores.
    """

    scores = []
    vars = vars.copy() # no modification on global vars

    if with_X:
        vars += X_vars
    for dat in dats:
        dat = shuffle(dat).reset_index() # add-on for random shuffling on trials

        X = np.column_stack([dat[var].values for var in vars])
        y = dat["RT"].values
        indiv_scores = cross_val_score(LinearRegression(), X, y, cv=n, scoring='r2')
        for score in indiv_scores:
            scores.append(score)
    return np.array(scores)

scores = cross_val(vars, n, with_X)
N_subj = len(scores)//n # number of subjects
print()
print("Model: RT ~ " + ("X + " if with_X else "") + " + ".join(vars))
print("Decay = " + str(decay) + " -> Accuracy (avg r2): %0.3f (+/- %0.3f), with 95%% confidence" % (scores.mean(), scores.std()/np.sqrt(N_subj) * 2))
