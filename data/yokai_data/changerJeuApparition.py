import os
import json

def mettre_a_jour_premiere_apparition():
    dossier_data = r"D:\MES PROJET\PROJET\API\yo-kai-API\data\yokai_data"
    fichiers_modifies = 0

    for fichier in os.listdir(dossier_data):
        if fichier.endswith('.json'):
            nom_sans_extension = os.path.splitext(fichier)[0]
            
            if nom_sans_extension.isdigit():
                yokai_id = int(nom_sans_extension)

                if 1 <= yokai_id < 983:
                    chemin_fichier = os.path.join(dossier_data, fichier)
                    
                    try:
                        with open(chemin_fichier, 'r', encoding='utf-8') as f:
                            data = json.load(f)

                        # data["premiere_apparition"] = "yww"
                        nomJeu = "ywb2"
                        # if data.get("premiere_apparition", "") == "yw2" : 
                        if "ywb1" in data.get("jeu_present", []) :
                            jeuPresent = data.get("jeu_present", [])
                            if nomJeu not in jeuPresent :
                                jeuPresent.append(nomJeu)
                                data["jeu_present"] = jeuPresent

                        with open(chemin_fichier, 'w', encoding='utf-8') as f:
                            json.dump(data, f, ensure_ascii=False, indent=4)
                        
                        fichiers_modifies += 1

                    except (json.JSONDecodeError, OSError) as e:
                        print(f"Erreur sur le fichier {fichier}: {e}")

    print(f"Terminé : {fichiers_modifies} fichier(s) mis à jour.")

if __name__ == "__main__":
    mettre_a_jour_premiere_apparition()