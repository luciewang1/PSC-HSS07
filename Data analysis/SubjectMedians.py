#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Agathe
"""

import FilterData as fd
import numpy as np
import matplotlib.pyplot as plt
import Medians as md
taux = 15
data_fichier = fd.import_good_enough_np(maxi=taux)

fig, (ax00, ax10, ax11) = plt.subplots(1, 3, sharey=True)
ecc = np.array([0, 3, 7])
stack10 = md.MedianeEccTousSujets(1, 0, data_fichier)
stack00 = md.MedianeEccTousSujets(0, 0, data_fichier)
stack11 = md.MedianeEccTousSujets(1, 1, data_fichier)

dic = {ax00: [stack00, "Flèches - Délai court"], ax10: [stack10,"AP - Délai court"], ax11: [stack11, "AP - Délai long"]}
for ax in dic:
    stack = dic[ax][0]
    for subject in stack :
        ax.plot(ecc, subject)
    ax.set_title(dic[ax][1])
    if ax == ax00 :
        ax.set_ylabel("RT(Alternance) - RT(Répétition)")
    ax.set_xlabel("Excentricité")
    ax.set_xticks((0,3,7))
    legend = str(len(stack)) + " sujets \ntaux d'erreur < " + str(taux) + "%"
    ax.text(0.5, 100, legend, fontsize=8)
plt.show()


