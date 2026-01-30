import urllib.request
import numpy as np

""" IMPORT DES DOCUMENTS """


URL_CSV = "https://raw.githubusercontent.com/gaetan-bv2005/P25-hackathon/main/sujet-9-clients.csv"

def lecture_cloud(url):
    with urllib.request.urlopen(url) as response:
        # On lit, on décode en texte, et on découpe par lignes
        content = response.read().decode('utf-8')
        return content.splitlines()
lignes = lecture_cloud(URL_CSV)
print(f"Chargement réussi : {len(lignes)} clients trouvés.")

print(lignes)

def dico(url):
    #créer une liste de dictionnaires : un dictionnaire par client
    sample = lecture_cloud(url)
    liste_dicos = []
    entetes = sample[0].split(",")
    for ligne in sample[1:]:
        valeurs = ligne.split(",")
        dico_ligne = {}
        for i, entete in enumerate(entetes):
            dico_ligne[entete] = valeurs[i]
        liste_dicos.append(dico_ligne)
    return liste_dicos

print(dico(URL_CSV))


""" CODE """

""" Fonctions et variables de base """"

usine={1:[217.876,7653.44,437,0,510.83]}

def distance (a,b) :
    return (abs((a[0]-b[0])**2 + (a[1]-b[1])**2))**0.5

def tempstrajet (a,b) :
    return distance(a,b)/70
