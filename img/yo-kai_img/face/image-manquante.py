import os

def trouver_images_manquantes(dossier_cible):
    # 1. Lister tous les fichiers du dossier
    fichiers = os.listdir(dossier_cible)
    
    nombres_trouves = []
    
    # 2. Extraire les numéros des fichiers .png
    for f in fichiers:
        if f.lower().endswith('.png'):
            # On enlève l'extension pour ne garder que le nom (ex: "12")
            nom_sans_extension = os.path.splitext(f)[0]
            
            # On vérifie si le nom est bien un nombre
            if nom_sans_extension.isdigit():
                nombres_trouves.append(int(nom_sans_extension))
    
    if not nombres_trouves:
        print("Aucune image numérotée n'a été trouvée dans le dossier.")
        return

    # 3. Déterminer la plage (du plus petit au plus grand nombre trouvé)
    min_num = min(nombres_trouves)
    max_num = max(nombres_trouves)
    
    tous_les_nombres_attendus = set(range(1, max_num + 1))
    nombres_manquants = tous_les_nombres_attendus - set(nombres_trouves)
    
    # 4. Afficher le résultat
    if nombres_manquants:
        print(f"--- Analyse terminée ---")
        print(f"Nombre d'images trouvées : {len(nombres_trouves)}")
        print(f"Numéros manquants ({len(nombres_manquants)}) :")
        print(sorted(list(nombres_manquants)))
    else:
        print("Parfait ! Aucun numéro ne manque dans la séquence.")

# --- CONFIGURATION ---
chemin_du_dossier = 'C:/Users/pacau/Desktop/MES PROJET/PROJET/API/yo-kai-API/img/yo-kai_img/face' 

trouver_images_manquantes(chemin_du_dossier)