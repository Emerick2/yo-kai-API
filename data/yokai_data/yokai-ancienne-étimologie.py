import os
import json
from datetime import datetime

DOSSIER = os.path.dirname(os.path.abspath(__file__))
NOMBRE = 100

AUJOURD_HUI = datetime.now().date()

yokai_sans_etimologie = []

for fichier in sorted(
    (nom for nom in os.listdir(DOSSIER) if nom.endswith(".json")),
    key=lambda nom: int(os.path.splitext(nom)[0]),
):
    chemin = os.path.join(DOSSIER, fichier)

    date_modification = datetime.fromtimestamp(
        os.path.getmtime(chemin)
    ).date()

    if date_modification == AUJOURD_HUI:
        continue

    with open(chemin, "r", encoding="utf-8") as f:
        donnees = json.load(f)

    yokais = donnees if isinstance(donnees, list) else [donnees]

    for yokai in yokais:
        if yokai.get("étimologie", "Inconnu") != "Inconnu" and yokai.get("étimologie", "Inconnu") != "":
            yokai_sans_etimologie.append({
                "Nom": yokai.get("Nom", "Inconnu"),
                "Description": yokai.get("Description", "Inconnu"),
                "étimologie": yokai.get("étimologie", "Inconnu"),
                "Fichier": fichier
            })

            if len(yokai_sans_etimologie) >= NOMBRE:
                break

    if len(yokai_sans_etimologie) >= NOMBRE:
        break

print(f"{len(yokai_sans_etimologie)} Yo-kai sans étymologie (fichiers modifiés aujourd'hui) :\n")

for yokai in yokai_sans_etimologie:
    print(f'{yokai["Nom"]} ({yokai["Fichier"]}) | Description : ({yokai["Description"]}) | étimologie ! ({yokai["étimologie"]})')