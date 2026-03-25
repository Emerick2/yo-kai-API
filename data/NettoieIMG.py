import os
import json

# Configuration
dossier_source = './' 
prefixe_url = "https://raw.githubusercontent.com/Emerick2/yo-kai-API/refs/heads/main/img/item-img/bug/"
extension = ".png"
fichier_sortie = "annuaire-img.json"

def traiter_fichiers_json():
    annuaire = {}

    # Lister les fichiers pour ne pas traiter le fichier de sortie s'il existe déjà
    fichiers = [f for f in os.listdir(dossier_source) if f.endswith('.json') and f != fichier_sortie]

    for nom_fichier in fichiers:
        chemin_complet = os.path.join(dossier_source, nom_fichier)
        
        try:
            with open(chemin_complet, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Gestion liste ou dictionnaire unique
            items = data if isinstance(data, list) else [data]

            for item in items:
                # On récupère le nom d'origine (ex: "Cigale verte")
                nom_image_origine = item.get("imageUrl")
                nom_entite = item.get("name")

                if nom_image_origine:
                    # 1. On crée l'URL complète
                    url_complete = f"{prefixe_url}{nom_image_origine}{extension}"
                    
                    # 2. On met à jour l'élément JSON avec l'URL complète
                    item["imageUrl"] = url_complete

                    # 3. On remplit l'annuaire avec le "name" et l'URL toute neuve
                    if nom_entite:
                        annuaire[nom_entite] = url_complete

            # On réécrit le fichier d'origine avec les URLs complètes
            with open(chemin_complet, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            
            print(f"✅ Mis à jour : {nom_fichier}")

        except Exception as e:
            print(f"❌ Erreur sur {nom_fichier} : {e}")

    # Écriture de l'annuaire final
    with open(fichier_sortie, 'w', encoding='utf-8') as f:
        json.dump(annuaire, f, indent=4, ensure_ascii=False)
    
    print(f"\n🚀 Annuaire généré avec {len(annuaire)} entrées dans {fichier_sortie}")

if __name__ == "__main__":
    traiter_fichiers_json()