import os
import json
import csv

# --- CONFIGURATION ---
JSON_DIR = '.' 
CSV_FILE = 'liste.csv'

def clean_val(val):
    """Nettoie les espaces et les retours à la ligne."""
    if val is None:
        return ""
    return val.strip()

def get_next_id():
    """Trouve le prochain ID disponible pour un nouveau fichier JSON."""
    files = [f for f in os.listdir(JSON_DIR) if f.endswith('.json') and f[:-5].isdigit()]
    if not files:
        return 1
    ids = [int(f[:-5]) for f in files]
    return max(ids) + 1

def update_or_create_yokai():
    yokai_db = []
    
    # 1. Charger les JSON existants
    for filename in os.listdir(JSON_DIR):
        if filename.endswith('.json') and filename[:-5].isdigit():
            file_path = os.path.join(JSON_DIR, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    yokai_db.append({'id': filename[:-5], 'data': data, 'path': file_path})
                except json.JSONDecodeError:
                    continue

    # 2. Lire le CSV
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            # Récupération des colonnes du CSV
            csv_en = clean_val(row.get('en', ''))
            csv_jp = clean_val(row.get('jp', ''))
            csv_romaji = clean_val(row.get('romaji-jp', '')) # Nouvelle colonne
            csv_fr = clean_val(row.get('fr', ''))

            # Recherche de correspondance
            matches = [
                y for y in yokai_db 
                if (csv_en and y['data'].get('nom_anglais') == csv_en) or 
                   (csv_jp and y['data'].get('nom_original') == csv_jp)
            ]

            if matches:
                for match in matches:
                    updated = False
                    
                    # Mise à jour du nom FR
                    if csv_fr and not clean_val(match['data'].get('Nom')):
                        match['data']['Nom'] = csv_fr
                        updated = True
                    
                    # Mise à jour du nom Anglais
                    if csv_en and not clean_val(match['data'].get('nom_anglais')):
                        match['data']['nom_anglais'] = csv_en
                        updated = True

                    # Mise à jour du nom Japonais
                    if csv_jp and not clean_val(match['data'].get('nom_original')):
                        match['data']['nom_original'] = csv_jp
                        updated = True
                    
                    # AJOUT : Mise à jour du Romaji s'il n'existe pas
                    if csv_romaji and not clean_val(match['data'].get('name_romaji_jp')):
                        match['data']['name_romaji_jp'] = csv_romaji
                        updated = True

                    if updated:
                        with open(match['path'], 'w', encoding='utf-8') as jf:
                            json.dump(match['data'], jf, ensure_ascii=False, indent=4)
                        print(f"Mis à jour : {match['id']}.json ({csv_en or csv_jp})")
            
            else:
                # Création d'un nouveau Yo-kai
                new_id = get_next_id()
                new_data = {
                    "Nom": csv_fr,
                    "nom_original": csv_jp,
                    "name_romaji_jp": csv_romaji, # Ajouté ici aussi
                    "nom_anglais": csv_en
                }
                new_filename = f"{new_id}.json"
                new_path = os.path.join(JSON_DIR, new_filename)
                
                with open(new_path, 'w', encoding='utf-8') as jf:
                    json.dump(new_data, jf, ensure_ascii=False, indent=4)
                
                yokai_db.append({'id': str(new_id), 'data': new_data, 'path': new_path})
                print(f"Créé : {new_filename} ({csv_en or csv_jp})")

if __name__ == "__main__":
    update_or_create_yokai()
    print("Mise à jour terminée avec les noms en Romaji !")