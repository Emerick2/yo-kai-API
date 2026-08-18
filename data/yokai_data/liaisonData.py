import os
import json
import re
import unicodedata

# Chemins des dossiers
DATA_DIR = r"D:\MES PROJET\PROJET\API\yo-kai-API\data\yokai_data"
OLD_DB_DIR = os.path.join(DATA_DIR, "yww complet")
LIAISON_FILE = os.path.join(OLD_DB_DIR, "liaison.json")

def make_an_url(valeur):
    valeur = unicodedata.normalize('NFD', str(valeur))
    valeur = re.sub(r'[\u0300-\u036f]', '', valeur)
    valeur = valeur.lower().strip()
    valeur = re.sub(r'\s+', '-', valeur)
    valeur = re.sub(r'[^\w\-]+', '', valeur)
    valeur = re.sub(r'--+', '-', valeur)
    return valeur

def nettoyer_cle(cle):
    """Supprime les traits d'union et tirets bas pour la comparaison de secours."""
    return cle.replace('-', '').replace('_', '')

def fusionner_bases():
    print("Début de la fusion...")
    if not os.path.exists(LIAISON_FILE):
        print(f"Fichier de liaison introuvable : {LIAISON_FILE}")
        return

    with open(LIAISON_FILE, "r", encoding="utf-8") as f:
        liaison = json.load(f)

    # Indexation de la nouvelle base de données
    index_nouvelle_db = {}
    index_sans_tiret = {}  # Index de secours (sans '-' ni '_')
    
    for element in os.listdir(DATA_DIR):
        chemin_complet = os.path.join(DATA_DIR, element)
        if os.path.isfile(chemin_complet) and element.endswith(".json"):
            try:
                with open(chemin_complet, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    
                nom_original = data.get("Nom")
                if nom_original:
                    nom_formate = make_an_url(nom_original)
                    index_nouvelle_db[nom_formate] = chemin_complet
                    
                    # Clé simplifiée sans traits d'union
                    cle_simple = nettoyer_cle(nom_formate)
                    index_sans_tiret[cle_simple] = chemin_complet
            except Exception as e:
                print(f"Erreur de lecture sur {element} : {e}")

    succes = 0
    erreurs = 0

    # Parcours du fichier de liaison
    for old_id, target_name in liaison.items():
        old_json_path = os.path.join(OLD_DB_DIR, f"{old_id}.json")
        
        if not os.path.exists(old_json_path):
            print(f"Fichier source introuvable : {old_id}.json")
            erreurs += 1
            continue

        # 1. Recherche directe avec la clé standard
        target_key = make_an_url(target_name)
        target_json_path = index_nouvelle_db.get(target_key) or index_nouvelle_db.get(target_name)

        # 2. Si non trouvé, tentative en enlevant les traits d'union / tirets bas
        if not target_json_path:
            target_key_simple = nettoyer_cle(target_key)
            target_json_path = index_sans_tiret.get(target_key_simple)
            if target_json_path:
                print(f"[Secours] Correspondance trouvée sans trait d'union pour ID {old_id} ({target_name})")

        if not target_json_path:
            print(f"Aucune correspondance trouvée dans l'API pour l'ID {old_id} ({target_name})")
            erreurs += 1
            continue

        # Fusion des données
        try:
            with open(old_json_path, "r", encoding="utf-8") as f_old:
                old_data = json.load(f_old)

            with open(target_json_path, "r", encoding="utf-8") as f_target:
                target_data = json.load(f_target)

            # Ajout des clés absentes uniquement
            modifie = False
            for key, value in old_data.items():
                if key not in target_data:
                    target_data[key] = value
                    modifie = True

            if modifie:
                with open(target_json_path, "w", encoding="utf-8") as f_target:
                    json.dump(target_data, f_target, ensure_ascii=False, indent=4)
                succes += 1
                print(f"Fusion : {old_id}.json -> {os.path.basename(target_json_path)}")
            else:
                print(f"Aucune nouvelle clé à ajouter pour {old_id}.json")

        except Exception as e:
            print(f"♦ Erreur lors de la fusion pour {old_id}.json : {e}")

    print(f"\nOpération terminée : {succes} fichiers mis à jour, {erreurs} ignorés/non trouvés.")

if __name__ == "__main__":
    fusionner_bases()