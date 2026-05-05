import os
import json
import shutil
import re
from pathlib import Path

# --- CONFIGURATION DES CHEMINS ---
# Utilisation de Path pour une meilleure compatibilité Windows/Linux
PATH_TEXTURES = Path("_3D/textures")
PATH_DATA = Path("yokai_data")
PATH_OUTPUT = Path("texture_renomer")

def rename_textures():
    # 1. Création du dossier de sortie s'il n'existe pas
    if not PATH_OUTPUT.exists():
        PATH_OUTPUT.mkdir(parents=True)
        print(f"Dossier créé : {PATH_OUTPUT}")

    # 2. Construction du dictionnaire de mapping {oldID: newID}
    # On parcourt tous les fichiers .json dans yokai_data
    mapping = {}
    if PATH_DATA.exists():
        for json_file in PATH_DATA.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    new_id = data.get("ID")
                    old_id = data.get("oldID")
                    
                    # On vérifie que les variables ne sont pas nulles
                    if new_id and old_id:
                        mapping[str(old_id)] = str(new_id)
            except Exception as e:
                print(f"Erreur lors de la lecture de {json_file}: {e}")

    if not mapping:
        print("Aucun mapping (oldID -> ID) trouvé dans les fichiers JSON.")
        return

    print(f"Mapping chargé : {mapping}")

    # 3. Traitement des images
    # Regex pour capturer l'ID (après le 'y') et le numéro de page
    # Exemple : texture_y3_01.png -> Group 1: 3, Group 2: 01
    pattern = re.compile(r"texture_y(\d+)_(\d+)\.png")

    count = 0
    if PATH_TEXTURES.exists():
        for img_path in PATH_TEXTURES.glob("*.png"):
            match = pattern.match(img_path.name)
            
            if match:
                current_old_id = match.group(1)
                page = match.group(2)

                # Si l'ID actuel correspond à un "oldID" dans notre mapping
                if current_old_id in mapping:
                    new_id = mapping[current_old_id]
                    new_filename = f"texture_y{new_id}_{page}.png"
                    
                    # Chemin de destination
                    dest_path = PATH_OUTPUT / new_filename
                    
                    # Copie et renommage
                    shutil.copy2(img_path, dest_path)
                    print(f"Renommé : {img_path.name} -> {new_filename}")
                    count += 1
                else:
                    # Optionnel : copier quand même si pas de changement ? 
                    # Ici on ne fait rien si l'ID n'est pas dans le mapping.
                    pass

    print(f"\nTerminé ! {count} images ont été traitées dans '{PATH_OUTPUT}'.")

if __name__ == "__main__":
    rename_textures()