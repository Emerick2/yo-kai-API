import os
import re
import unicodedata
import json
from pathlib import Path

import requests
from bs4 import BeautifulSoup
import shutil
import copy
import html

def make_an_url(valeur):
    """Transforme une chaîne de caractères en slug (ex: 'Jibanyan' -> 'jibanyan')."""
    valeur = unicodedata.normalize('NFD', str(valeur))
    valeur = re.sub(r'[\u0300-\u036f]', '', valeur)
    valeur = valeur.lower().strip()
    valeur = re.sub(r'\s+', '-', valeur)
    valeur = re.sub(r'[^\w\-]+', '', valeur)
    valeur = re.sub(r'--+', '-', valeur)
    return valeur

def main():
    base_url = "https://emerick2.github.io/yo-kai-API"
    dossier_json = Path("data/yokai_data")

    categories = [
        {"dir": "img/yo-kai_img/picture", "ext": ".png", "json_key": "image_url", "prefix": ""},
        {"dir": "img/yo-kai_img/medals", "ext": ".png", "json_key": "medals", "prefix": ""},
        {"dir": "img/yo-kai_img/face", "ext": ".png", "json_key": "face", "prefix": ""},
        {"dir": "song/yo-kai-song", "ext": ".wav", "json_key": "song", "prefix": ""},
        {"dir": "img/yo-kai_img/special_medals", "ext": ".png", "json_key": None, "prefix": ""},
        {"dir": "img/card", "ext": ".webp", "json_key": None, "prefix": "yokai_card_"}
    ]

    if not dossier_json.exists():
        print(f"Erreur : Le dossier {dossier_json} n'existe pas.")
        return

    for json_file in dossier_json.glob('*.json'):
        yokai_id = json_file.stem 

        # 1. Lire le fichier JSON
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            print(f"⚠️ Erreur de lecture du fichier : {json_file}")
            continue

        # 2. Récupérer le nom et créer le slug (fallback sur l'ID si le nom n'existe pas)
        nom = data.get("Nom", yokai_id)
        slug = make_an_url(nom)

        print(f"--- Traitement de [{yokai_id}] : {nom} -> {slug} ---")

        # 3. Traiter chaque catégorie d'image / son
        for cat in categories:
            dossier = Path(cat["dir"])
            prefix = cat["prefix"]
            ext = cat["ext"]
            json_key = cat["json_key"]

            old_filename = f"{prefix}{yokai_id}{ext}"
            
            if json_key and data.get(json_key):
                url_actuelle = data.get(json_key)
                old_filename = url_actuelle.split('/')[-1]

            old_file_path = dossier / old_filename
            new_file_path = dossier / f"{prefix}{slug}{ext}"

            if old_file_path.exists():
                if new_file_path.exists():
                    print(f"  [Déjà traité] {new_file_path} existe déjà. Passage à la suite.")
                else:
                    old_file_path.rename(new_file_path)
                    print(f"  [Renommé] {old_file_path} -> {new_file_path}")
            elif new_file_path.exists():
                print(f"  [Info] Le fichier est déjà nommé {new_file_path.name}")


            # 4. Mettre à jour la valeur dans le dictionnaire JSON
            if json_key:
                nouvelle_url = f"{base_url}/{cat['dir']}/{prefix}{slug}{ext}"
                data[json_key] = nouvelle_url

        # 5. Sauvegarder les modifications dans le fichier JSON
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"  [Mis à jour] JSON sauvegardé pour {nom}.")

    print("\n✅ Terminé ! Tous les fichiers ont été renommés et les JSON ont été mis à jour.")

if __name__ == "__main__":
    main()