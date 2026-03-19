import json
import os
import sys

# --- CONFIGURATION LA REQUÊTE ---
DOSSIER_DATA = "../yokai_data"
NOM_FICHIER_CIBLE = "yo-kai-tribue-Sinistre.json"
CRITERE = "Tribue"
VALEUR = "Sinistre"

def Ecrire(message):
    """Affiche un message sur une seule ligne en effaçant la précédente."""
    sys.stdout.write(f"\r{message}")
    sys.stdout.flush()

def filtrer_yokai(dossier_source, fichier_destination, cle_critere, valeur_attendue):
    resultats = []
    
    fichiers = [f for f in os.listdir(dossier_source) if f.endswith('.json')]
    total = len(fichiers)

    for index, nom_fichier in enumerate(fichiers, 1):
        Ecrire(f"Progression : {index}/{total} (Traitement de {nom_fichier})...")
        
        chemin_complet = os.path.join(dossier_source, nom_fichier)
        try:
            with open(chemin_complet, 'r', encoding='utf-8') as f:
                donnees = json.load(f)
                
                if donnees.get(cle_critere) == valeur_attendue:
                    identifiant = donnees.get("ID")
                    if identifiant:
                        resultats.append(identifiant)
        except Exception:
            pass

    print("\nExtraction terminée !")

    with open(fichier_destination, 'w', encoding='utf-8') as f_dest:
        json.dump(resultats, f_dest, indent=4, ensure_ascii=False)
    
    print(f"Total : {len(resultats)} IDs de Yo-kai (Rang {valeur_attendue}) enregistrés dans {fichier_destination}.")

if __name__ == "__main__":
    filtrer_yokai(DOSSIER_DATA, NOM_FICHIER_CIBLE, CRITERE, VALEUR)