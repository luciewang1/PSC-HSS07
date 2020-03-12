#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
script to plot the boxplots of DeltaRTs for every possible conditions (motricity, excentricity, delay)

@author: Agathe
"""

import FilterData as fd
import numpy as np
import matplotlib.pyplot as plt
import Medians as md
taux = 15
data_fichier = fd.import_good_enough_np(maxi= taux)

fig, (ax00, ax10, ax11) = plt.subplots(1, 3, sharey=True, )
ecc = np.array([0, 3, 7])
stack10 = md.MedianeEccTousSujets(1, 0, data_fichier)
stack00 = md.MedianeEccTousSujets(0, 0, data_fichier)
stack11 = md.MedianeEccTousSujets(1, 1, data_fichier)

dic = {ax00: [stack00, "Flèches - Délai court"], ax10: [stack10,"AP - Délai court"], ax11: [stack11, "AP - Délai long"]}
for ax in dic:
    stack = dic[ax][0]
    ax.boxplot([stack[:, 0], stack[:, 1], stack[:, 2]], labels = [0,3,7])
    ax.set_title(dic[ax][1])
    if ax == ax00 :
        ax.set_ylabel("RT(Alternance) - RT(Répétition)")
    ax.set_xlabel("Excentricité")
    legend = str(len(stack)) + " sujets \ntaux d'erreur < " + str(taux) + "%"
    ax.text(1, 100, legend, fontsize=8, color = 'blue')
plt.show()