from pathlib import Path

def lecture(filename):
    sample = Path(filename).read_text().splitlines()
    return sample

print(lecture("sujet-9-clients.csv"))

