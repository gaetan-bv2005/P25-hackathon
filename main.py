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
Longueur = len(dico(URL_CSV))
print(dico(URL_CSV))


""" CODE """
# CLASSE CLIENT

class Client :
    def __init__(self, id_client, coord_x, coord_y, init, capacity, consumption, statut):
        self.id_client = id_client
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.init = init
        self.capacity = capacity
        self.consumption = consumption
        self.statut = statut
    def __str__(self):
        return f"Client {self.id_client} : coord_x={self.coord_x}, coord_y={self.coord_y}, init={self.init}, capacity={self.capacity}, consumption={self.consumption}, statut={self.consumption}"

    def liste_clients():
        dictionnaire = dico(URL_CSV)
        L_clients = []
        for i in range (Longueur):
            cl = Client(
                id_client = i+1,
                coord_x = dictionnaire[i]["coord_x"],
                coord_y = dictionnaire[i]["coord_y"],
                init = dictionnaire[i]["init"],
                capacity = dictionnaire[i]["capacity"],
                consumption = dictionnaire[i]["consumption"]
                statut = False
            )
            L_clients.append(cl)
        return L_clients
print(Client.liste_clients()[2])

""" Fonctions et variables de base """"

usine={1:[217.876,7653.44,437,0,510.83]}

def distance (a,b) :
    return (abs((a.coord_x-b.coord_x)**2 + (a.coord_y-b.coord_y)**2))**0.5

def tempstrajet (a,b) :
    return distance(a,b)/70





