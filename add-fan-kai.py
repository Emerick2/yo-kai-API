# CSV_FILE = "main.csv"
# TEMP_IMG = "main.png"

import os
import json
import csv
import shutil
import re
import unicodedata

def make_an_url(valeur):
    valeur = unicodedata.normalize('NFD', str(valeur))
    valeur = re.sub(r'[\u0300-\u036f]', '', valeur)
    valeur = valeur.lower().strip()
    valeur = re.sub(r'\s+', '-', valeur)
    valeur = re.sub(r'[^\w\-]+', '', valeur)
    valeur = re.sub(r'--+', '-', valeur)
    return valeur

def clean_key(text):
    text = text.replace("(nombre)", "").strip()
    text = "".join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    text = text.lower().replace(" ", "-")
    text = re.sub(r'[^a-z0-9-]', '', text)
    return text

def clean_value(value, is_number=False):
    if not value:
        return 0 if is_number else ""
    
    clean_val = value.replace("\n", " ").replace("\r", " ").strip()
    
    if is_number:
        try:
            num_match = re.search(r'\d+', clean_val)
            return int(num_match.group()) if num_match else 0
        except ValueError:
            return 0
    return clean_val

def addFanKai():
    PATH_ANNUAIRE = "data/annuaire_fan-kai.json"
    DIR_DATA = "data/fankai_data/"
    DIR_IMG_LOCAL = "fan-kai_img"
    DIR_IMG_ABSOLUTE = r"C:\Users\pacau\Desktop\MES PROJET\PROJET\WEB\wikinyan\wikinyan\img\fan-kai_img"
    CSV_FILE = "main.csv"
    TEMP_IMG = "main.png"

    # S'assurer que les dossiers existent
    os.makedirs(DIR_DATA, exist_ok=True)
    os.makedirs(DIR_IMG_LOCAL, exist_ok=True)
    if not os.path.exists(DIR_IMG_ABSOLUTE):
        print(f"Attention : Le chemin absolu {DIR_IMG_ABSOLUTE} n'est pas accessible.")

    # --- 1. Lecture du CSV ---
    raw_data = {}
    try:
        with open(CSV_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if len(row) >= 2:
                    key, value = row[0].strip(), row[1].strip()
                    if "Déposer les" in key:
                        continue
                    raw_data[key] = value
    except FileNotFoundError:
        print("Erreur : main.csv introuvable.")
        return

    if os.path.exists(PATH_ANNUAIRE):
        with open(PATH_ANNUAIRE, 'r', encoding='utf-8') as f:
            annuaire = json.load(f)
    else:
        annuaire = []

    nom_yokai = raw_data.get("Nom")
    if not nom_yokai:
        print("Erreur : Le nom du Yo-kai est manquant dans le CSV.")
        return

    existing_entry = next((item for item in annuaire if item["nom"] == nom_yokai), None)
    
    if existing_entry:
        yokai_id = existing_entry["id"]
        print(f"Mise à jour du Yo-kai : {nom_yokai} (ID: {yokai_id})")
    else:
        yokai_id = max([item["id"] for item in annuaire], default=0) + 1
        annuaire.append({"id": yokai_id, "nom": nom_yokai})
        print(f"Ajout d'un nouveau Yo-kai : {nom_yokai} (ID: {yokai_id})")

    final_data = {}
    for key, value in raw_data.items():
        is_num = "(nombre)" in key
        new_key = clean_key(key)
        final_data[new_key] = clean_value(value, is_number=is_num)

    with open(f"{DIR_DATA}{yokai_id}.json", 'w', encoding='utf-8') as f:
        json.dump(final_data, f, indent=4, ensure_ascii=False)

    with open(PATH_ANNUAIRE, 'w', encoding='utf-8') as f:
        json.dump(annuaire, f, indent=4, ensure_ascii=False)

    if os.path.exists(TEMP_IMG):
        img_name = f"{make_an_url(nom_yokai)}.png"
        
        shutil.copy(TEMP_IMG, os.path.join(DIR_IMG_LOCAL, img_name))
        
        try:
            if os.path.exists(os.path.dirname(DIR_IMG_ABSOLUTE)):
                shutil.copy(TEMP_IMG, os.path.join(DIR_IMG_ABSOLUTE, img_name))
        except Exception as e:
            print(f"Erreur lors de la copie vers le dossier Bureau : {e}")
        
        print(f"Image traitée : {img_name}")
    else:
        print("Note : Aucune image 'img.png' trouvée, étape ignorée.")

    print("Opération terminée avec succès.")

if __name__ == "__main__":
    addFanKai()