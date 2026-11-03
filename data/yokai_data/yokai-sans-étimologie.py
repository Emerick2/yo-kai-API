import os
import json

DOSSIER = os.path.dirname(os.path.abspath(__file__))
NOMBRE = 100

yokai_sans_etimologie = []

for fichier in sorted(
    (nom for nom in os.listdir(DOSSIER) if nom.endswith(".json")),
    key=lambda nom: int(os.path.splitext(nom)[0]),
):
    chemin = os.path.join(DOSSIER, fichier)

    with open(chemin, "r", encoding="utf-8") as f:
        donnees = json.load(f)

    yokais = donnees if isinstance(donnees, list) else [donnees]

    for yokai in yokais:
        if not (yokai.get("étimologie") or "").strip():
            yokai_sans_etimologie.append({
                "Nom": yokai.get("Nom", "Inconnu"),
                "Description": yokai.get("Description", "Inconnu"),
                "Fichier": fichier
            })

            if len(yokai_sans_etimologie) >= NOMBRE:
                break

    if len(yokai_sans_etimologie) >= NOMBRE:
        break

print(f"{len(yokai_sans_etimologie)} Yo-kai sans étymologie :\n")

for yokai in yokai_sans_etimologie:
    print(f'{yokai["Nom"]} ({yokai["Fichier"]}) | Description : ({yokai["Description"]})')