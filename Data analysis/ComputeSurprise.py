# programme retournant les surprises théoriques à chaque instant

## Import packages

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

#specific to data analysis
from utils import import_one_subject, get_serie_data
from FilterData import import_good_enough_pd, info_data

# specific to toolbox (Meyniel)
from MarkovModel_Python import IdealObserver as IO
from MarkovModel_Python import GenerateSequence as sg

def ():


# Set parameters on experience
maxi = 15       # maximum pourcentage of errors allowed
exp_type = None # 1 for delay, 0 for motricity, None for both

# Set parameters of the model
decay = 16 #comme discuté, paramètre de la décroissance exp
order = 1  #on regarde les probas de transition

#import data
df = import_good_enough_pd(maxi, exp_type)

seq =  #séquence des signaux (rond/carré) à extraire de df !!! il faut 1 sequence np.array !!!

seq = sg.ConvertSequence(seq)['seq'] #converti la s"quences en 0/1; tout roule ensuite

options = {'Decay': decay, 'p_c': 1, 'resol': 1}  # seul decay est utile, marche en enlevant les autres du dico ?
out_fixed = IO.IdealObserver(seq, 'fixed', order=order, options=options)
surprise = out_fixed['surprise'] #surprise théorique, calculée par la méthode ci dessus

# ajouter ces surprsises au data frame. surprise correspond à la surprise théorique, à chaque instant, associée à la séquence seq.