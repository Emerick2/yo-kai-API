import os
import json

def creer_annuaire():
    dossier_source = 'yokai_data'
    fichier_sortie = 'annuaire_yo-kai.json'
    annuaire = {}

    if not os.path.exists(dossier_source):
        print(f"Erreur : Le dossier '{dossier_source}' est introuvable.")
        return

    for nom_fichier in os.listdir(dossier_source):
        if nom_fichier.endswith('.json'):
            chemin_complet = os.path.join(dossier_source, nom_fichier)
            
            yokai_id = os.path.splitext(nom_fichier)[0]
            
            try:
                with open(chemin_complet, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    nom_yokai = data.get("Nom", "Nom inconnu")
                    
                    annuaire[yokai_id] = nom_yokai
            except Exception as e:
                print(f"Erreur lors de la lecture de {nom_fichier} : {e}")

    with open(fichier_sortie, 'w', encoding='utf-8') as f_out:
        json.dump(annuaire, f_out, indent=4, ensure_ascii=False)

    print(f"Succès ! L'annuaire a été créé : {fichier_sortie}")

if __name__ == "__main__":
    creer_annuaire()