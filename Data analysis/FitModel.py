#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DONE SO FAR
For any given model, evaluate goodness of fit to experimental data, by cross-validation over all subjects (sci-kit learn library).
Input: model defined by its set of variables vars
Output: its average R2 score over all subjects

TO DO
For two given models (say A, B), implement a t-test on their difference of scores (R2_A - R2_B) across all subjects.
Input: two models defined by their sets of variables (vars_A and vars_B)
Goal: determine if there is a significant difference between R2_A and R2_B across all subjects

Further details (from Florent Meyniel):
le test pertinent ici est de calculer la significativité de la différence appariée.
Autrement dit, vous calculez pour chaque sujet la différence de R2 entre les deux modèles, puis tester au niveau du groupe,
par un t-test, si cette différence est significative
(il existe aussi des fonctions de t-test appariée dans lesquelles vous données vos deux listes de R2,
chacune présentant les sujets dans le même ordre, et la fonction calcule toute seule la significativité de la différence appariée).

Parameters details (apart from vars, all parameters should stick to their current value):
List of our models under study:
0. []
1. ["surprise"]
2. ["rep"]
3. ["rep_center", "rep_later"]
4. ["center", "rep_center", "rep_later"]
5. ["center", "rep_center", "rep_later", "surprise"]
T-test should be carried out between models:
- 0 and 1
- 4 and 5
- 2 and 3
- 3 and 4
"""

#import os
from utils import import_one_subject, get_serie_data
from FilterData import import_good_enough_pd#, info_data
import numpy as np
import pandas as pd
import scipy.stats as stats
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
decay = 16
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
    Cross-validate a linear model over all subjects, by aggregating cross-validation scores obtained individually.
    Input: list of regressor variables (strings), number of folds for n-fold cross-validation, base regressors X (True if to be included).
    Output: array of R2 scores (one score by subject).
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
print("Decay = " + str(decay) + " -> Accuracy (avg R2): %0.3f (+/- %0.3f), with 95%% confidence" % (scores.mean(), scores.std()/np.sqrt(N_subj) * 2))



def t_test(vars_A,vars_B, n=5, with_X=True):
    """
    We suppose that the samples of the models are always related
    Input:2 different list of regressor variables (strings), number of folds for n-fold cross-validation, base regressors X (True if to be included).
    Output:(t-statistic,p-value)
    """
    return stats.ttest_rel(cross_val(vars_A,n,with_X),cross_val(vars_B,n,with_X))

VARS=[[],["surprise"],["rep"],["rep_center", "rep_later"],["center", "rep_center", "rep_later"]
                                  ,["center", "rep_center", "rep_later", "surprise"]]

#T-Tests between different models
for i in range(5):
    if(i!=1):
        print()
        print("t-test between model "+repr(i)+" and model "+ repr(i+1)+" : ")
        print(t_test(VARS[i],VARS[i+1]))