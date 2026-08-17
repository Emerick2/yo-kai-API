import json
import os
from pathlib import Path

from DEV.trieParRang import La_MainTrieCategorie

BASE_DIR = Path(__file__).resolve().parent


def creer_annuaire(versionAnglais: bool):
    dossier_source = BASE_DIR / "yokai_data"
    fichier_sortie = BASE_DIR / "annuaire_yo-kai.json"
    if versionAnglais:
        fichier_sortie = BASE_DIR / "annuaire_yo-kai_anglais.json"

    annuaire = {}

    if not dossier_source.exists():
        print(f"Erreur : Le dossier '{dossier_source}' est introuvable.")
        return

    for nom_fichier in sorted(os.listdir(dossier_source)):
        if nom_fichier.endswith('.json'):
            chemin_complet = dossier_source / nom_fichier
            yokai_id = os.path.splitext(nom_fichier)[0]

            try:
                with open(chemin_complet, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    nom_yokai = data.get("Nom", "Nom inconnu")
                    if versionAnglais:
                        nom_yokai = data.get("nom_anglais", "Nom inconnu")

                    annuaire[yokai_id] = nom_yokai
            except Exception as e:
                print(f"Erreur lors de la lecture de {nom_fichier} : {e}")

    with open(fichier_sortie, 'w', encoding='utf-8') as f_out:
        json.dump(annuaire, f_out, indent=4, ensure_ascii=False)

    print(f"Succès ! L'annuaire a été créé : {fichier_sortie}")


def LaMainCompleteAnuaire():
    creer_annuaire(False)
    creer_annuaire(True)
    La_MainTrieCategorie()


if __name__ == "__main__":
    LaMainCompleteAnuaire()