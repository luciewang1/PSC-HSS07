import utils
import numpy as np
import os
rootdir = "C:/Users/Agathe/PycharmProjects/PSC/data/allData"
data_fichier = []
# faire une liste de toutes les données.
files = os.listdir(rootdir)
for filename in files:
    data_fichier.append(utils.import_one_subject(rootdir, filename))


# calcul des médianes pour chaque excentriccités
import matplotlib.pyplot as plt
def medianeEcc(motor,delay,data):
    """input :
     motor = la condition motrice 0 ou 1
     delay = 0 ou 1 (delay long ou court)
     data = les données d'UN participant
     output : tab
     le tableau des médianes en fonction de l'excentricité
    """

    tab = [0, 0, 0]
    for ecc in range (3):
        ind = (data["motor"] == motor) & (data["delay"] == delay)
        eccent = data["ecc"] == ecc
        rep = (data["rep"] == 'True') & ind & eccent & (data["Correct"] == 1)
        alt = (data["rep"] == 'False') & ind & eccent & (data["Correct"] == 1)
        dataRep = data["RT"][rep]
        dataAlt = data["RT"][alt]
        # ignore lines where they were no answer :
        dataRep = dataRep[ dataRep != -1]
        dataAlt = dataAlt[dataAlt != -1]
        tab[ecc] = np.median(dataRep) - np.median(dataAlt)

    return tab

fig, (ax1,ax2) = plt.subplots(1,2,sharey=True)
# les eccentricités en abscisses
ecc = np.array([0, 3, 7])
for sujet in data_fichier:
    if utils.sujetAdmissible(sujet) :
        med = medianeEcc(1, 0, sujet)
        stack = np.concatenate((stack, np.array([med])), axis=0)
        ax1.plot(ecc, med )
print(np.shape(stack))
print(stack)
med = np.median(stack,0)
ax2.boxplot([stack[:,0], stack[:,1], stack[:,2]])
#ax2.errorbar(ecc,med, yerr = np.quantile(stack,0.75,axis=0))
plt.show()


