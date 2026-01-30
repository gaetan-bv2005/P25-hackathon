from pathlib import Path

def lecture(filename):
    sample = Path(filename).read_text().splitlines()
    return sample

print(lecture("sujet-9-clients.csv"))


try:
    with open("C:\\Users\\gaeta\\Documents\\MINES\\Nouveau dossier\\port-energy-sim\\P25-hackathon\\sujet-9-clients.csv", "r", encoding="utf-8") as fichier:
        lignes = fichier.readlines()
        for ligne in lignes:
            print(ligne.strip())


