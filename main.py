import urllib.request

# Remplace par ton lien "Raw" copié
URL_CSV = "https://raw.githubusercontent.com/gaetan-bv2005/P25-hackathon/main/sujet-9-clients.csv"

def lecture_cloud(url):
    with urllib.request.urlopen(url) as response:
        # On lit, on décode en texte, et on découpe par lignes
        content = response.read().decode('utf-8')
        return content.splitlines()

# Maintenant, n'importe qui avec internet peut lancer ça !
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
