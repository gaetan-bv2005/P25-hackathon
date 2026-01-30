import urllib.request
import numpy as np

#IMPORT DES DOCUMENTS

log = open("log.txt", "w")

URL_CSV = "https://raw.githubusercontent.com/gaetan-bv2005/P25-hackathon/main/sujet-9-clients.csv"

def lecture_cloud(url):
    with urllib.request.urlopen(url) as response:
        content = response.read().decode('utf-8')
        return content.splitlines()

def dico(url):
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


""" CODE """

class camion :
    def __init__(self,coord_x,coord_y,nb_bouteilles_vides,nb_bouteilles_pleines,destination,en_chemin,t):
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.nb_bouteilles_vides = nb_bouteilles_vides
        self.nb_bouteilles_pleines = nb_bouteilles_pleines
        self.destination = destination
        self.en_chemin = en_chemin
        self.t = t

#on créer tous les camions
Camions ={}

for i in range (30):
    Camions[i] =  camion(0,0,10,20,0,True,0)
    if Camions[i].nb_bouteilles_pleines+Camions[i].nb_bouteilles_vides > 80:
        raise ValueError("Le camion ne peut pas transporter plus de 80 bouteilles au total.")

#coordonnées de l'usine
x_usine=217.876
y_usine=6753.44


# CLASSE CLIENT
class Client :
    def __init__(self, id_client, coord_x, coord_y, nb_vides, nb_pleines, capacity, consumption, statut):
        self.id_client = id_client
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.nb_vides = nb_vides
        self.nb_pleines = nb_pleines
        self.capacity = capacity
        self.consumption = consumption
        self.statut = statut
    def __str__(self):
        return f"Client {self.id_client}"

def liste_clients():
    dictionnaire = dico(URL_CSV)
    L_clients = []
    for i in range (Longueur):
        cl = Client(
            id_client = i+1,
            coord_x = float(dictionnaire[i]["coord_x"]),
            coord_y = float(dictionnaire[i]["coord_y"]),
            nb_vides = 0, # Au début on suppose 0 vides
            nb_pleines = int(dictionnaire[i]["init"]), # Init correspond aux pleines
            capacity = int(dictionnaire[i]["capacity"]),
            consumption = float(dictionnaire[i]["consumption"]),
            statut = False
        )
        L_clients.append(cl)
    return L_clients
clients = liste_clients()

#positions initiales des camions
for i in range (30):
    Camions[i].coord_x= ((clients[i].coord_x)+x_usine)/2
    Camions[i].coord_y= ((clients[i].coord_y)+y_usine)/2
    Camions[i].destination=clients[i].id_client
    Camions[i].t= np.sqrt((Camions[i].coord_x-clients[i].coord_x)**2+(Camions[i].coord_x-clients[i].coord_x)**2)/70
    Camions[i].coord_x= clients[i].coord_x
    Camions[i].coord_y= clients[i].coord_y


""" Fonctions et variables de base """

usine=Client(1000,217.876,7653.44,0,437,100000,510.83,False)

def distance (a,b) :
    return np.sqrt(abs((a.coord_x-b.coord_x)**2 + (a.coord_y-b.coord_y)**2))

def tempstrajet (a,b) :
    return distance(a,b)/70

def trouvertmin () : 
    minimum=1000000
    indicemin=0
    for i in range(len(Camions)) :
        if Camions[i].t<minimum :
            minimum=Camions[i].t
            indicemin=i
    return [minimum, indicemin]

def update_T() : # Update les tmin de chaque camion
    for key, item in Camions.items() :
        item.t=item.t-resultat_tmin[0]

def update_stock(tmin) : 
    for client in clients:
        conso = client.consumption * tmin
        client.nb_pleines -= conso
        client.nb_vides += conso
        if client.nb_pleines < 0:
            client.nb_pleines = 0
    usine.nb_pleines += usine.consumption*tmin


def calcul_n_livrable(camion, client):
    place_libre_camion = 80 - (camion.nb_bouteilles_pleines + camion.nb_bouteilles_vides)
    nb_vides_recuperables = min(client.nb_vides, place_libre_camion)
    vides_restantes_chez_client = client.nb_vides - nb_vides_recuperables
    place_physique_dispo = client.capacity - (client.nb_pleines + vides_restantes_chez_client)
    n = min(camion.nb_bouteilles_pleines, place_physique_dispo)
    return max(0, n)

def cible(liste_clients, cam): 
    clients_enattente = [] 
    for client in clients:
        if client.statut == False :
            clients_enattente.append(client)
    if cam.nb_bouteilles_vides > cam.nb_bouteilles_pleines :
        return 1000 #=usine.id_client 
    else :
        rapport = [] 
        indices_valides = []
        for i, client in enumerate(clients_enattente):
            n = calcul_n_livrable(cam,client)
            d = distance(cam,client)
            if d > 0:
                rapport.append(n/d)
                indices_valides.append(i)
        
        if not rapport: return 1000

        max_val = rapport[0]
        cible_client = clients_enattente[indices_valides[0]]

        for i in range(len(rapport)):
            if rapport[i]>max_val :
                max_val = rapport[i]
                cible_client = clients_enattente[indices_valides[i]]
        
        cam.en_chemin = True
        clients[cible_client.id_client - 1].statut = True 
        return cible_client.id_client


horloge=0
G=0

dico_temps={} 
for i in range(len(Camions)) :
    dico_temps[i]=[0]

dico_log={} 
for i in range(len(Camions)) :
    dico_log[i]=[] # Correction ici pour initialiser correctement

resultat_tmin = [0, 0] # Init pour entrer dans la boucle

while horloge < 1000: # Augmenté un peu le temps pour voir la simu
    
    resultat_tmin=trouvertmin () 
    
    # Petite sécurité si t=0 pour éviter la boucle infinie
    if resultat_tmin[0] == 0:
        pass

    horloge +=resultat_tmin[0]
    
    client_livre = Camions[resultat_tmin[1]].destination 
    update_T() 
    update_stock(resultat_tmin[0]) 

    if client_livre != 1000: # Le client livré n'est pas l'usine
        idx = client_livre - 1
        nombre_bouteilles_pleines_données_par_le_camion = min(clients[idx].capacity-clients[idx].nb_pleines,Camions[resultat_tmin[1]].nb_bouteilles_pleines)
        Camions[resultat_tmin[1]].nb_bouteilles_pleines = Camions[resultat_tmin[1]].nb_bouteilles_pleines - nombre_bouteilles_pleines_données_par_le_camion
        clients[idx].nb_pleines = clients[idx].nb_pleines + nombre_bouteilles_pleines_données_par_le_camion
        nombre_bouteilles_vides_récupérées_par_le_camion = min(clients[idx].nb_vides,80-Camions[resultat_tmin[1]].nb_bouteilles_vides-Camions[resultat_tmin[1]].nb_bouteilles_pleines) 
        Camions[resultat_tmin[1]].nb_bouteilles_vides += nombre_bouteilles_vides_récupérées_par_le_camion
        G=G+200*nombre_bouteilles_pleines_données_par_le_camion-0.7*distance(Camions[resultat_tmin[1]],clients[idx])
        
        # Mise à jour position physique du camion
        Camions[resultat_tmin[1]].coord_x = clients[idx].coord_x
        Camions[resultat_tmin[1]].coord_y = clients[idx].coord_y
        clients[idx].statut = False 

    else :
        Camions[resultat_tmin[1]].nb_bouteilles_vides = 0
        Camions[resultat_tmin[1]].nb_bouteilles_pleines = 80
        G=G-0.7*distance(Camions[resultat_tmin[1]],usine)
        # Mise à jour position physique du camion (Usine)
        Camions[resultat_tmin[1]].coord_x = x_usine
        Camions[resultat_tmin[1]].coord_y = y_usine

    dico_temps[resultat_tmin[1]].append(horloge)
    
    dest=""  
    
    if Camions[resultat_tmin[1]].coord_x == x_usine and Camions[resultat_tmin[1]].coord_y == y_usine :
        dest="P"
    else :
        dest="C"

    id="" 
    if  Camions[resultat_tmin[1]].destination ==1000 :
        id="1"
    else :
        id=str(Camions[resultat_tmin[1]].destination)

    delta_t = abs(dico_temps[resultat_tmin[1]][-1]-dico_temps[resultat_tmin[1]][-2]) if len(dico_temps[resultat_tmin[1]]) > 1 else 0
    
    ligne_a_ecrire = f"{dico_temps[resultat_tmin[1]][-1]}:{dest}{id}/{delta_t}+{nombre_bouteilles_vides_récupérées_par_le_camion}-{nombre_bouteilles_pleines_données_par_le_camion} "
    
    dico_log[resultat_tmin[1]].append(ligne_a_ecrire)

    # réafectation de la cible du camion
    nouvelle_cible = cible(liste_clients,Camions[resultat_tmin[1]])
    
    Camions[resultat_tmin[1]].destination = nouvelle_cible

    # On calcule la distance entre le camion (qui est maintenant à l'ancienne cible) et la nouvelle cible
    objet_cible = None
    if nouvelle_cible == 1000:
        objet_cible = usine
    else:
        objet_cible = clients[nouvelle_cible - 1]
    
    Camions[resultat_tmin[1]].t = tempstrajet(Camions[resultat_tmin[1]], objet_cible) # Mise à jour du temps t pour que le camion reparte

for i in dico_log.keys() :
    for j in dico_log[i]:
        log.write(j)
    log.write("\n")
log.close()
print("Terminé")
