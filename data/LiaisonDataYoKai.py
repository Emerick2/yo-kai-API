import json
import os
import re

MAPPING_FILE = os.path.join("_3D", "yokai_assets_mapping.json")
YOKAI_DIR = "yokai_data"

FIELDS_TO_COPY = [
    "Tribue", "Rang", "PV", "Force", "Esprit", "Défense", "Vitesse",
    "nourriture", "élément", "Rôle", "talent", "Technique", "Type",
    "nourriture_favorite", "attaques", "phrases_nourriture", "voix",
    "tribu_yw4", "attaques_par_jeu", "soul_effects", "drops", "special_talent"
]

def is_empty(val):
    if val is None:
        return True
    if isinstance(val, str) and val.strip() == "":
        return True
    if isinstance(val, list) and len(val) == 0:
        return True
    if isinstance(val, dict) and len(val) == 0:
        return True
    return False

def main():
    if not os.path.exists(MAPPING_FILE):
        print(f"Erreur : Le fichier de mapping '{MAPPING_FILE}' est introuvable.")
        return

    with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
        mapping = json.load(f)

    for dest_id in range(727, 794):
        dest_id_str = str(dest_id)
        if dest_id_str not in mapping:
            continue

        model_file = mapping[dest_id_str].get("modelFile", "")
        # Extraire l'ID du yo-kai d'origine à partir du nom du fichier modèle (ex: model_y197.fbx -> 197)
        match = re.search(r"model_y(\d+).*?\.fbx", model_file)
        if not match:
            print(f"Impossible de déduire la source pour {dest_id_str} à partir de {model_file}")
            continue

        source_id_str = match.group(1)
        
        source_path = os.path.join(YOKAI_DIR, f"{source_id_str}.json")
        dest_path = os.path.join(YOKAI_DIR, f"{dest_id_str}.json")

        if not os.path.exists(source_path):
            print(f"Fichier source {source_path} introuvable.")
            continue
        if not os.path.exists(dest_path):
            print(f"Fichier destination {dest_path} introuvable.")
            continue

        with open(source_path, 'r', encoding='utf-8') as f:
            source_data = json.load(f)
        with open(dest_path, 'r', encoding='utf-8') as f:
            dest_data = json.load(f)

        updated = False
        for field in FIELDS_TO_COPY:
            if field in source_data:
                source_val = source_data[field]
                dest_val = dest_data.get(field)

                if not is_empty(dest_val):
                    if dest_val == source_val:
                        continue # La valeur est déjà la même
                    
                    # Demander confirmation avant d'écraser
                    # print(f"\n[Yo-kai {dest_id_str} (copie de {source_id_str})] Conflit pour le champ '{field}' :")
                    # print(f"  - Valeur actuelle : {dest_val}")
                    # print(f"  - Nouvelle valeur (source) : {source_val}")
                    # rep = input("Faut-il écraser la valeur actuelle ? (o/n) : ").strip().lower()
                    # if rep == 'o':
                    #     dest_data[field] = source_val
                    #     updated = True
                else:
                    dest_data[field] = source_val
                    updated = True

        if updated:
            with open(dest_path, 'w', encoding='utf-8') as f:
                json.dump(dest_data, f, indent=4, ensure_ascii=False)
            print(f"-> Yo-kai {dest_id_str} mis à jour avec succès.")

if __name__ == "__main__":
    main()
