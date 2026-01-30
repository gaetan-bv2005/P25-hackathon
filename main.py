

try:
    with open("C:\\Users\\gaeta\\Documents\\MINES\\Nouveau dossier\\port-energy-sim\\P25-hackathon\\sujet-9-clients.csv", "r", encoding="utf-8") as fichier:
        lignes = fichier.readlines()
        for ligne in lignes:
            print(ligne.strip())


