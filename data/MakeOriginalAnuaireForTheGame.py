import os
import json

def generer_annuaire_jeu(dossier_data, jeu_clef, fichier_sortie):
    yokai_trouves = {}

    if not os.path.exists(dossier_data):
        print(f"Erreur : Le dossier '{dossier_data}' n'existe pas.")
        return

    for filename in os.listdir(dossier_data):
        if filename.endswith('.json'):
            chemin_fichier = os.path.join(dossier_data, filename)
            
            try:
                with open(chemin_fichier, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                medallium_ids = data.get("medallium_ids", {})
                
                if jeu_clef in medallium_ids and medallium_ids[jeu_clef]:
                    raw_id = medallium_ids[jeu_clef]
                    id_str = "".join(filter(str.isdigit, raw_id.split("-")[0]))
                    
                    if id_str:
                        id_num = int(id_str)
                        nom = data.get("Nom", "Inconnu")
                        yokai_trouves[id_num] = nom
                            
            except (json.JSONDecodeError, ValueError, KeyError) as e:
                print(f"Fichier {filename} ignoré en raison d'une erreur : {e}")

    liste_ordonnee = []
    compteur_inconnus_consecutifs = 0
    id_actuel = 1

    while compteur_inconnus_consecutifs <= 30:
        if yokai_trouves and id_actuel > max(yokai_trouves.keys()) - compteur_inconnus_consecutifs:
            restants = [k for k in yokai_trouves.keys() if k >= id_actuel]
            if not restants or min(restants) - id_actuel > 30:
                break

        if id_actuel in yokai_trouves:
            liste_ordonnee.append(yokai_trouves[id_actuel])
            compteur_inconnus_consecutifs = 0
        else:
            liste_ordonnee.append("inconnu")
            compteur_inconnus_consecutifs += 1
        
        id_actuel += 1

    while liste_ordonnee and liste_ordonnee[-1] == "inconnu":
        liste_ordonnee.pop()

    structure_finale = {
        "yo-kai": liste_ordonnee,
        "boss": []
    }

    with open(fichier_sortie, 'w', encoding='utf-8') as f:
        json.dump(structure_finale, f, ensure_ascii=False, indent=4)

    print(f"Annuaire généré ! S'est arrêté à l'ID {id_actuel - compteur_inconnus_consecutifs - 1} suite à un trou de plus de 30 inconnus.")

# --- Configuration et Exécution ---
DOSSIER_INPUT = "yokai_data"
JEU_CIBLE = "YW3"
FICHIER_OUTPUT = f"annuaire_{JEU_CIBLE.lower()}.json"

generer_annuaire_jeu(DOSSIER_INPUT, JEU_CIBLE, FICHIER_OUTPUT)