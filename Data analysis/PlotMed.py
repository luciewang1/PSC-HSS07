#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
script pour afficher les graphes (1 par type d'expérience) des DeltaRTs en fonction de l'excentricité

@author: Agathe
"""

import FilterData as fd
import numpy as np
import matplotlib.pyplot as plt
import Medians as md

data = fd.import_good_enough_np(maxi=20)

ecc = np.array([0, 3, 7])
stack10 = md.MedianeEccTousSujets(1, 0, data)
stack00 = md.MedianeEccTousSujets(0, 0, data)
stack11 = md.MedianeEccTousSujets(1, 1, data)
fig, (mot,tim) = plt.subplots(1,2, sharey= True)
# Affichage courbes moyennes - motricité

mot.errorbar(ecc, md.meanSD(stack10)[0], yerr = md.meanSD(stack10)[1], label="Motricité 1 - Delay 0")
mot.errorbar(ecc + 0.06, md.meanSD(stack00)[0], yerr = md.meanSD(stack00)[1], label="Motricité 0 - Delay 0")
# Légendes et titres
mot.set_title("Expérience de type Motricité")
mot.set_xticks((0,3,7))
mot.grid(True)
mot.text(4,-20, "1-0 : " + str(len(stack10)) + " sujets \n0-0 : "+str(len(stack00)) + " sujets", fontsize = 8)
mot.legend()

# Affichage courbes moyennes - Delay
tim.errorbar(ecc, md.meanSD(stack10)[0], yerr = md.meanSD(stack10)[1], label="Motricité 1 - Delay 0")
tim.errorbar(ecc + 0.06, md.meanSD(stack11)[0], yerr = md.meanSD(stack11)[1], label="Motricité 1 - Delay 1")
# Légendes et titres
tim.set_title("Expérience de type Delay")
tim.set_xticks((0,3,7))
tim.text(4,-20, "1-0 : " + str(len(stack10)) + " sujets \n1-1 : "+str(len(stack11)) + " sujets", fontsize = 8)
tim.grid(True)
tim.legend()

plt.show()