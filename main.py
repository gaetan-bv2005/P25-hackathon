from pathlib import Path

def lecture(filename):
    sample = Path(filename).read_text().splitlines()
    return sample

print(lecture("sujet-9-clients.csv"))

def dico(filename):
    #créer une liste de dictionnaires : un dictionnaire par client
    sample = lecture(filename)
    liste_dicos = []
    entetes = sample[0].split(",")
    for ligne in sample[1:]:
        valeurs = ligne.split(",")
        dico_ligne = {}
        for i, entete in enumerate(entetes):
            dico_ligne[entete] = valeurs[i]
        liste_dicos.append(dico_ligne)
    return liste_dicos
print(dico("sujet-9-clients.csv"))
