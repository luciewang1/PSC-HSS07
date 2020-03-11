# auteur : Agathe
# Fonction : visualiser les courbes RT(rep) - RT(alt) en fonction de l'exccentricité pour chaque type d'expérience


import utils
import FilterData as fd
import numpy as np
import os

data_fichier = fd.import_good_enough_np(maxi=20)

# calcul des médianes pour chaque excentriccités
import matplotlib.pyplot as plt


def medianeEcc(motor, delay, data):
    """input :
     motor = la condition motrice 0 ou 1
     delay = 0 ou 1 (delay long ou court)
     data = les données d'UN participant
     output : tab
     liste des médianes en fonction de l'excentricité
    """

    tab = [0, 0, 0]
    for ecc in range(3) :
        ind = (data["motor"] == motor) & (data["delay"] == delay)
        eccent = data["ecc"] == ecc
        rep = (data["rep"] == 1) & ind & eccent & (data["Correct"] == 1)
        alt = (data["rep"] == 0) & ind & eccent & (data["Correct"] == 1)
        dataRep = data["RT"][rep]
        dataAlt = data["RT"][alt]
        # ignore lines where they were no answer :
        dataRep = dataRep[dataRep != -1]
        dataAlt = dataAlt[dataAlt != -1]
        # Calculer la différence de médianes
        tab[ecc] = np.median(dataRep) - np.median(dataAlt)

    return tab


def MedianeEccTousSujets(motor, delay, data_fichier) :
    """Renvoie un numpy.array stack où chaque ligne correspond au medianeEcc d'un sujet"""
    stack = np.array([[0, 0, 0]])
    for sujet in data_fichier :

        med = medianeEcc(motor, delay, sujet)
        if np.isfinite(med[0]) :
            stack = np.concatenate((stack, np.array([med])), axis=0)

    return stack


# Graphiques :
fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
ecc = np.array([0, 3, 7])
stack10 = MedianeEccTousSujets(1, 0, data_fichier)
stack00 = MedianeEccTousSujets(0, 0, data_fichier)
stack11 = MedianeEccTousSujets(1, 1, data_fichier)
stack = stack10
print(stack)
# Visualisation des courbes individuelles et boîtes à moustaches
for med in stack :
    ax1.plot(ecc, med)
    # affichages des boites à moustaches
ax2.boxplot([stack[:, 0], stack[:, 1], stack[:, 2]])
# légendes et titres
ax1.set_title("Courbes individuelles R-A fonction de l'excentricité")
ax2.set_title("Boxplots")
ax1.set_ylabel("RT(Alternance) - RT(Répétition)")
ax1.set_xlabel("Excentricité")
ax2.set_xlabel("Excentricité")


# Calcul des moyennes par colonne
def meanSD(stack) :
    return np.mean(stack, 0), np.std(stack, 0) / np.sqrt(len(stack))


# affichage courbes moyennes - motricité
figmot, (mot) = plt.subplots()
mot.errorbar(ecc, meanSD(stack10)[0], yerr=meanSD(stack10)[1], label="Motricité 1 - Delay 0")
mot.errorbar(ecc + 0.04, meanSD(stack00)[0], yerr=meanSD(stack00)[1], label="Motricité 0 - Delay 0")
# Légendes et titres
mot.set_title("Moyennes des $\Delta$RT en fonction de la motricité")
mot.grid(True)
mot.legend()

# Affichage courbes moyennes - Delay
figTiming, (tim) = plt.subplots()
tim.errorbar(ecc, meanSD(stack10)[0], yerr=meanSD(stack10)[1], label="Motricité 1 - Delay 0")
tim.errorbar(ecc + 0.04, meanSD(stack11)[0], yerr=meanSD(stack11)[1], label="Motricité 1 - Delay 1")
# Légendes et titres
tim.set_title("Moyennes des $\Delta$RT en fonction du temps inter-stimuli")
tim.grid(True)
tim.legend()

plt.show()
