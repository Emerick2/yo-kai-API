import os
import json

LOCAL_DATA_PATH = "C:/Users/pacau/Desktop/MES PROJET/PROJET/API/yo-kai-API/data/yokai_data"

def charger_tous_les_yokai():
    """Charge tous les Yo-kai en mémoire pour pouvoir chercher par nom rapidement."""
    yokai_files = {}
    if not os.path.exists(LOCAL_DATA_PATH):
        print(f"❌ Erreur : Le dossier {LOCAL_DATA_PATH} n'existe pas.")
        return yokai_files

    for filename in os.listdir(LOCAL_DATA_PATH):
        if filename.endswith(".json"):
            filepath = os.path.join(LOCAL_DATA_PATH, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    nom = data.get("Nom")
                    if nom:
                        # On stocke le nom en minuscule pour ignorer la casse lors de la recherche
                        yokai_files[nom.lower()] = {
                            "filename": filename,
                            "filepath": filepath,
                            "data": data
                        }
            except Exception as e:
                print(f"⚠️ Impossible de lire {filename}: {e}")
    return yokai_files

def editeur_medallium():
    print("🔍 Chargement de la base de données Wikinyan...")
    base_yokai = charger_tous_les_yokai()
    print(f"✅ {len(base_yokai)} Yo-kai chargés. Prêt à l'édition !\n")
    print("💡 Astuce : Tape 'quitter' ou 'exit' pour arrêter le programme.\n")

    jeu = input("🎮 Quel jeu voulez-vous éditer ? (ex: YW, YW3, YW4) : ").strip()
    if not jeu:
        print("⚠️ Opération annulée (nom de jeu vide).\n")
        return
    
    while True:
        recherche = input("📝 Entrez le nom du Yo-kai à modifier : ").strip()
        
        if recherche.lower() in ["quitter", "exit", ""]:
            print("👋 Fin de l'édition. À bientôt !")
            break

        if recherche.lower() not in base_yokai:
            print(f"❌ Aucun Yo-kai trouvé avec le nom '{recherche}'. Réessaie.\n")
            continue

        yokai_selectionne = base_yokai[recherche.lower()]
        data = yokai_selectionne["data"]
        filepath = yokai_selectionne["filepath"]
        
        print(f"\n✨ Yo-kai trouvé dans {yokai_selectionne['filename']} :")
        print(f"   Nom original : {data.get('Nom')}")
        
        if "medallium_ids" not in data or not isinstance(data["medallium_ids"], dict):
            data["medallium_ids"] = {}
            
        print("   Numéros actuels :", json.dumps(data["medallium_ids"], ensure_ascii=False))

        

        nouveau_num = input(f"🔢 Entrez le nouveau numéro pour {jeu} (ou Entrée pour laisser vide) : ").strip()

        # Mise à jour de la valeur
        if nouveau_num == "":
            if jeu in data["medallium_ids"]:
                del data["medallium_ids"][jeu]
                print(f"🗑️ Numéro supprimé pour {jeu}.")
        else:
            data["medallium_ids"][jeu] = nouveau_num
            print(f"✅ Mis à jour : {jeu} -> {nouveau_num}")

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"💾 Fichier sauvegardé avec succès !\n")
            
            base_yokai[recherche.lower()]["data"] = data
            
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde du fichier : {e}\n")

if __name__ == "__main__":
    editeur_medallium()