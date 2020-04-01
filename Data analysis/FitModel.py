#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fit the Minimal Transitions Probabilities Model to experimental data.
    - import data with surprise column
    - conduct linear regression on.

TO DO:
    - cross-validate the fitted model, within individual data
    - analyze performance of the fit, by operating cross-validation over all subjects
    - extra: analyze inter-subject variance? extract numbers of interest from results, see how they vary from one subject to another
"""

import os
from utils import import_one_subject, get_serie_data
from FilterData import import_good_enough_pd, info_data
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import scipy.stats as stats
#import researchpy as rp
import statsmodels.api as sm
from statsmodels.formula.api import ols

def fit_model(dat):
    """
    Conduct linear regression of RT from individual data.
    Input: dataframe for one subject, having a surprise column.
    Output: results (statsmodels format).
    """

    model = ols('RT ~ rep + surprise', data = dat)
    results = model.fit()
    return results

dat = import_one_subject("../Data/Session 1", "firstexample_01_202001221414.xpd", with_surprise=True)
print(dat)
print(fit_model(dat).summary())