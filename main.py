import urllib.request
import numpy as np

""" IMPORT DES DOCUMENTS """

log = open("log.txt", "x")

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



class camion :
    def __init__(self,coord_x,coord_y,nb_bouteilles_vides,nb_bouteilles_pleines,destination,en_chemin,t):

        self.coord_x = coord_x#coordonnées de la destination
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

print(Camions)
        



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
        return f"Client {self.id_client} : coord_x={self.coord_x}, coord_y={self.coord_y}, nb_vides={self.nb_vides}, nb_pleines={self.nb_pleines}, capacity={self.capacity}, consumption={self.consumption}, statut={self.consumption}"

    
def liste_clients():
    dictionnaire = dico(URL_CSV)
    L_clients = []
    for i in range (Longueur):
        cl = Client(
            id_client = i+1,
            coord_x = float(dictionnaire[i]["coord_x"]),
            coord_y = float(dictionnaire[i]["coord_y"]),
            nb_vides = int(dictionnaire[i]["init"]),
            nb_pleines = 0,
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

def trouvertmin () : #renvoie [tmin,indice du camion tq tmin] (TROUVE QUEL CAMION ARRIVE EN PREMIER)
    L=[]
    minimum=Camions[0].t
    indicemin=0
    for i in range(len(Camions)) :
        if Camions[i].t<minimum :
            minimum=Camions[i].t
            indicemin=i
    return [minimum, i]

resultat_tmin=trouvertmin () 

def update_T() : # Update les tmin de chaque camion
    for i in Camions.keys() :
        i.t=i.t-resultat_tmin[0]
    

def update_stock(tmin) : #après avoir déterminer tmin, on udpate les stocks des clients et de l'usine pour que les soustractions dans les camions soient les bonnes
    for client in liste_clients:
        client.init -= client.consumption * tmin
        if client.init < 0:
            client.init = 0
    usine.init += usine.comsuption*tmin


#Fonction qui définit la cible vers lequel le camion dispo va se dirigier, et renvoie les coordonnées de cette cible
x_usine = 217.876
y_usine = 7653.44

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
        rapport = [] #on regarde pour chaque client la valeur du rapport nombre de bouteilles pleines à livrer / distance au client et on renvoie la position du client qui maximise ce rapport
        for client in clients_enattente:
            n = calcul_n_livrable(cam,client)
            rapport.append(n/distance(cam,client))
        max = rapport[0]
        for i in range(len(rapport)):
            if rapport[i]>max :
                max = rapport[i]
                cible_client = clients_enattente[i]   #on regarde quel client a le meilleur rapport
        cam.en_chemin = True
        clients[cible_client.id_client - 1].statut = True  #on met à jour le statut du client dans la liste des clients
        return cible_client.id_client


horloge=0
G=0

dico_temps={} #Ce dico va stocker pour chaqsue camion, le temps auquel il s'est arreté la dèrnirère fois
for i in range(len(Camions)) :
    dico_temps[i]=[0]
    
while horloge < 30*24: #il limite le nombre d'itérations que va réaliser le programme 
    horloge +=resultat_tmin[0]
    resultat_tmin=trouvertmin () #on cherche le camion qui arrive en premier
    client_livre = Camions[resultat_tmin[1]].destination #on récupère l'indice de la destination du camion qui arrive en premier
    update_T() #on update les tmin des camion
    update_stock(resultat_tmin[0]) #on met à jour les stocks des clients et de l'usine durant le temps tmin

    if client_livre != 1000: # Le client livré n'est pas l'usine
        nombre_bouteilles_pleines_données_par_le_camion = min(client_livre.capacity-client_livre.nb_pleines,Camions[resultat_tmin[1]].nb_bouteilles_pleines)
        Camions[resultat_tmin[1]].nb_bouteilles_pleines = Camions[resultat_tmin[1]].nb_bouteilles_pleines - nombre_bouteilles_pleines_données_par_le_camion
        client_livre.nb_pleines = client_livre.nb_pleines + nombre_bouteilles_pleines_données_par_le_camion
        nombre_bouteilles_vides_récupérées_par_le_camion = min(client_livre.nb_vides,80-Camions[resultat_tmin[1]].nb_bouteilles_vides-Camions[resultat_tmin[1]].nb_bouteilles_pleines) #on récupère le nombre de bouteilles vides que le client doit donner
        Camions[resultat_tmin[1]].nb_bouteilles_vides += nombre_bouteilles_vides_récupérées_par_le_camion
        G=G+200*nombre_bouteilles_pleines_données_par_le_camion-0.7*distance(Camions[resultat_tmin[1]],clients[client_livre])




    else :
        Camions[resultat_tmin[1]].nb_bouteilles_vides = 0
        Camions[resultat_tmin[1]].nb_bouteilles_pleines = 80
        G=G-0.7*distance(Camions[resultat_tmin[1]],usine)

    dico_temps[resultat_tmin[1]].append(horloge)
    
    dest=""  ####DESTINATION = usine ou client
    
    if Camions[resultat_tmin[1]].coord_x == xusine and Camions[resultat_tmin[1]].coord_y == yusine :
        dest="P"
    else :
        dest="C"

    id="" ##### DESTINATION NUMERO (=1000 POUR USINE)
    if  Camions[resultat_tmin[1]].destination ==1000 :
            id="1"
    else :
            id=char(Camions[resultat_tmin[1]].destination)

    log.write(dico_temps[resultat_tmin[1]][-2],":",dest,id,"/",abs(dico_temps[resultat_tmin[1]][-1]-dico_temps[resultat_tmin[1]][-1]),"+",nombre_bouteilles_vides_récupérées_par_le_camion,"-",nombre_bouteilles_pleines_données_par_le_camion,"\n") 

    #réafectation de la cible du camion
    nouvelle_cible = cible(liste_clients,Camions[resultat_tmin[1]])
    Camions[resultat_tmin[1]].destination = nouvelle_cible
    
log.close()







