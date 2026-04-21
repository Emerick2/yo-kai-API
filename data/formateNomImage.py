import os
import re
import json
import unicodedata
from pathlib import Path
from urllib.parse import unquote

def make_an_url(valeur):
    valeur = unquote(unquote(valeur))
    
    nom_fichier, extension = os.path.splitext(valeur)
    extension = extension.lower()

    nom_fichier = nom_fichier.replace('_', '-').replace('%3f', '').replace('%3F', '')

    valeur = unicodedata.normalize('NFD', nom_fichier)
    valeur = re.sub(r'[\u0300-\u036f]', '', valeur)
    
    valeur = valeur.lower().strip()
    
    valeur = re.sub(r'[^a-z0-9\-]', '', valeur)
    
    valeur = re.sub(r'-+', '-', valeur).strip('-')
    
    valeur = valeur.replace("d27","")
    valeur = valeur.replace("l27","")
    return valeur + extension

def process_cleaning():
    img_dir = "C:/Users/pacau/Desktop/MES PROJET/PROJET/API/yo-kai-API/img/item-img/bug" #input("Entrez le chemin du dossier des IMAGES : ").strip()
    json_dir = "C:/Users/pacau/Desktop/MES PROJET/PROJET/API/yo-kai-API/data/bug_data" #input("Entrez le chemin du dossier des JSON : ").strip()

    img_path = Path(img_dir)
    json_path = Path(json_dir)

    if not img_path.exists() or not json_path.exists():
        print("❌ Erreur de dossier.")
        return

    mapping = {}

    print("\n--- 1. Renommage des images ---")
    for img_file in img_path.iterdir():
        # print(img_file)
        if img_file.suffix.lower() in ('.png', '.jpg', '.webp'):
            ancien_nom = img_file.name
            nouveau_nom = make_an_url(ancien_nom)
            
            nouveau_chemin = img_file.parent / nouveau_nom
            
            if ancien_nom != nouveau_nom:
                try:
                    if nouveau_chemin.exists():
                        os.remove(nouveau_chemin)
                    
                    os.rename(img_file, nouveau_chemin)
                    mapping[ancien_nom] = nouveau_nom
                    print(f"✅ {ancien_nom} -> {nouveau_nom}")
                except Exception as e:
                    print(f"⚠️ Erreur : {e}")
            else:
                mapping[ancien_nom] = nouveau_nom

    print("\n--- 2. Mise à jour des JSON ---")
    for j_file in json_path.glob("*.json"):
        with open(j_file, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except: continue

        if "imageUrl" in data:
            url_complete = data["imageUrl"]
            nom_image_url = url_complete.split('/')[-1]
            
            nouveau_nom_calcule = None
            
            for ancien_nom_reel, nouveau_nom_propre in mapping.items():
                if unquote(nom_image_url).lower() == unquote(ancien_nom_reel).lower():
                    nouveau_nom_calcule = nouveau_nom_propre
                    break
            
            if nouveau_nom_calcule:
                prefixe = "/".join(url_complete.split('/')[:-1])
                data["imageUrl"] = f"{prefixe}/{nouveau_nom_calcule}"
                
                with open(j_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                print(f"📝 {j_file.name} mis à jour : {nouveau_nom_calcule}")

if __name__ == "__main__":
    process_cleaning()