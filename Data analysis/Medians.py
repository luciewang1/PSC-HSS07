# auteur : Agathe
# deux fonctions utiles pour calculer les différences de médianes RT entre alternance et répétition


import numpy as np


# calcul des médianes pour chaque excentriccités

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


# Calcul des moyennes par colonne
def meanSD(stack) :
    return np.mean(stack, 0), np.std(stack, 0) / np.sqrt(len(stack))



