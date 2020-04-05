#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module to add a surprise column to individual data.
"""

import numpy as np
import pandas as pd

from MarkovModel_Python import IdealObserver as IO
from MarkovModel_Python import GenerateSequence as sg

def add_surprise(dat, decay=16, order=1):
    """
    Add theoretical surprise (-log(prob)) to individual data, according to the Minimal Transition Probabilities Model reset at every new series.
    Input: data dictionary (by attribute) of lists (by trial) for one subject, decay parameter for the model, order for the model.
    Output: same data dictionary updated.
    """

    options = {'Decay': decay}
    seq = dat["seq"]
    surprise = [] # list for theoretical surprises
    for seriesId in range(12):
        seqSeries = seq[seriesId*120:(seriesId+1)*120]
        seqSeries = sg.ConvertSequence(seqSeries)['seq']  # seq : stimuli sequence (1/0 for square/disk)

        out_fixed = IO.IdealObserver(seqSeries, 'fixed', order=order, options=options)
        surprise += list(out_fixed['surprise'])
    dat["surprise"] = surprise
    return dat