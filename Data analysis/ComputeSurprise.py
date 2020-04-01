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
    Add theoretical surprise to individual data, according to the Minimal Transition Probabilities Model.
    Input: data dictionary (by attribute) of lists (by trial) for one subject, decay parameter for the model, order for the model.
    Output: same data dictionary updated.
    """

    seq = dat["seq"]
    seq = sg.ConvertSequence(seq)['seq'] # seq : séquence des signaux (1/0 pour rond/carré)

    options = {'Decay': decay}
    out_fixed = IO.IdealObserver(seq, 'fixed', order=order, options=options)
    surprise = out_fixed['surprise'] # surprise théorique, calculée par la méthode ci dessus
    dat["surprise"] = surprise
    return dat