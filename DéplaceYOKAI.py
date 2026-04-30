import os
import json
import glob
import shutil

BASE_URL = "https://emerick2.github.io/yo-kai-API"
MAPPING_FILE = "data/_3D/yokai_assets_mapping.json"
TEMP_ID = 999999  

def _load_mapping():
    """Charge le fichier JSON de mapping 3D s'il existe."""
    if os.path.exists(MAPPING_FILE):
        with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def _save_mapping(mapping):
    """Sauvegarde le fichier JSON de mapping 3D."""
    os.makedirs(os.path.dirname(MAPPING_FILE), exist_ok=True)
    with open(MAPPING_FILE, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)

def _update_yokai_json(filepath, old_id, new_id):
    """Met à jour le contenu du fichier data.json d'un Yo-kai."""
    if not os.path.exists(filepath):
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if "oldID" not in data:
        data["oldID"] = data.get("ID", str(old_id))
        
    data["ID"] = str(new_id)
    data["image_url"] = f"{BASE_URL}/img/yo-kai_img/picture/{new_id}.png"
    data["medals"] = f"{BASE_URL}/img/yo-kai_img/medals/{new_id}.png"
    data["face"] = f"{BASE_URL}/img/yo-kai_img/face/{new_id}.png"
    data["song"] = f"{BASE_URL}/song/yo-kai-song/{new_id}.wav"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def _move_yokai_assets(old_id, new_id, mapping):
    """Déplace physiquement les fichiers d'un ID vers un autre et met à jour le mapping."""
    paths_to_move = [
        (f"data/yokai_data/{old_id}.json", f"data/yokai_data/{new_id}.json"),
        (f"img/yo-kai_img/face/{old_id}.png", f"img/yo-kai_img/face/{new_id}.png"),
        (f"img/yo-kai_img/medals/{old_id}.png", f"img/yo-kai_img/medals/{new_id}.png"),
        (f"img/yo-kai_img/picture/{old_id}.png", f"img/yo-kai_img/picture/{new_id}.png"),
        (f"img/yo-kai_img/special_medals/{old_id}.png", f"img/yo-kai_img/special_medals/{new_id}.png"),
        (f"song/yo-kai-song/{old_id}.wav", f"song/yo-kai-song/{new_id}.wav"),
        (f"data/_3D/models/model_y{old_id}.fbx", f"data/_3D/models/model_y{new_id}.fbx")
    ]
    
    # 1. Déplacer les fichiers standards
    for old_p, new_p in paths_to_move:
        if os.path.exists(old_p):
            os.makedirs(os.path.dirname(new_p), exist_ok=True)
            shutil.move(old_p, new_p)
            
    # 2. Déplacer les textures (gestion de multiples fichiers avec glob)
    old_tex_pattern = f"data/_3D/models/texture_y{old_id}_*.png"
    for old_tex in glob.glob(old_tex_pattern):
        # Récupère la fin du nom (ex: "01.png")
        suffix = old_tex.split(f"texture_y{old_id}_")[-1]
        new_tex = f"data/_3D/models/texture_y{new_id}_{suffix}"
        shutil.move(old_tex, new_tex)
        
    # 3. Mettre à jour le contenu du fichier JSON
    _update_yokai_json(f"data/yokai_data/{new_id}.json", old_id, new_id)
    
    # 4. Mettre à jour le dictionnaire de mapping 3D
    old_model_name = f"model_y{old_id}.fbx"
    new_model_name = f"model_y{new_id}.fbx"
    
    # Déplacer la clé principale dans le mapping
    if str(old_id) in mapping:
        mapping[str(new_id)] = mapping.pop(str(old_id))
        
    # Mettre à jour les références croisées des modèles/textures pour TOUS les autres Yo-kais
    for key, asset_data in mapping.items():
        if asset_data.get("modelFile") == old_model_name:
            asset_data["modelFile"] = new_model_name
        
        if "textureFiles" in asset_data:
            new_textures = []
            for tex in asset_data["textureFiles"]:
                if tex.startswith(f"texture_y{old_id}_"):
                    new_tex = tex.replace(f"texture_y{old_id}_", f"texture_y{new_id}_")
                    new_textures.append(new_tex)
                else:
                    new_textures.append(tex)
            asset_data["textureFiles"] = new_textures

def deplaceYokai(ID_depart, ID_arrive, justeIntervertire):
    mapping = _load_mapping()
    
    if justeIntervertire:
        # Échange simple utilisant un espace temporaire pour ne rien écraser
        _move_yokai_assets(ID_depart, TEMP_ID, mapping)
        _move_yokai_assets(ID_arrive, ID_depart, mapping)
        _move_yokai_assets(TEMP_ID, ID_arrive, mapping)
    else:
        # Insertion avec décalage
        _move_yokai_assets(ID_depart, TEMP_ID, mapping)
        
        if ID_depart > ID_arrive:
            # Décaler vers le haut : de ID_arrive jusqu'à ID_depart - 1
            for i in range(ID_depart - 1, ID_arrive - 1, -1):
                _move_yokai_assets(i, i + 1, mapping)
        elif ID_depart < ID_arrive:
            # Décaler vers le bas : de ID_depart + 1 jusqu'à ID_arrive
            for i in range(ID_depart + 1, ID_arrive + 1):
                _move_yokai_assets(i, i - 1, mapping)
                
        _move_yokai_assets(TEMP_ID, ID_arrive, mapping)
        
    _save_mapping(mapping)
    print(f"✅ Déplacement du Yo-kai {ID_depart} vers {ID_arrive} terminé.")


def ajouterYokai(ID_arrive):
    mapping = _load_mapping()
    
    # 1. Trouver le dernier ID existant pour savoir jusqu'où décaler
    max_id = 1
    while os.path.exists(f"data/yokai_data/{max_id}.json"):
        max_id += 1
    max_id -= 1  # Le dernier ID valide
    
    # 2. Faire de la place : décaler tous les Yo-kai de 1 rang vers le haut
    if max_id >= ID_arrive:
        for i in range(max_id, ID_arrive - 1, -1):
            _move_yokai_assets(i, i + 1, mapping)
            
    # 3. Placer les nouveaux fichiers depuis le dossier newYK
    new_assets = [
        ("newYK/data.json", f"data/yokai_data/{ID_arrive}.json"),
        ("newYK/face.png", f"img/yo-kai_img/face/{ID_arrive}.png"),
        ("newYK/medals.png", f"img/yo-kai_img/medals/{ID_arrive}.png"),
        ("newYK/picture.png", f"img/yo-kai_img/picture/{ID_arrive}.png"),
        ("newYK/special_medals.png", f"img/yo-kai_img/special_medals/{ID_arrive}.png"),
        ("newYK/song.wav", f"song/yo-kai-song/{ID_arrive}.wav"),
        ("newYK/model.fbx", f"data/_3D/models/model_y{ID_arrive}.fbx")
    ]
    
    textures = glob.glob("newYK/texture_*.png")
    for old_tex in textures:
        # Assumant que le fichier s'appelle newYK/texture_01.png
        suffix = old_tex.split("_")[-1] 
        new_assets.append((old_tex, f"data/_3D/models/texture_y{ID_arrive}_{suffix}"))
        
    # Copie et création du mapping pour le nouveau Yo-kai
    texture_list_for_mapping = []
    
    for old_p, new_p in new_assets:
        if os.path.exists(old_p):
            os.makedirs(os.path.dirname(new_p), exist_ok=True)
            shutil.copy(old_p, new_p) # copy au lieu de move pour préserver newYK si besoin
            
            if "texture_" in new_p:
                texture_list_for_mapping.append(os.path.basename(new_p))
                
    # 4. Mettre à jour le JSON du petit nouveau
    _update_yokai_json(f"data/yokai_data/{ID_arrive}.json", ID_arrive, ID_arrive)
    
    # 5. Ajouter l'entrée dans le mapping
    if os.path.exists(f"newYK/model.fbx"):
        mapping[str(ID_arrive)] = {
            "modelFile": f"model_y{ID_arrive}.fbx",
            "textureFiles": texture_list_for_mapping
        }
        
    _save_mapping(mapping)
    print(f"✅ Ajout du nouveau Yo-kai à l'ID {ID_arrive} terminé.")

#ID_depart, ID_arrive, justeIntervertire
# attention il faut viser l'ID-1 parce qu'il seront décaler vers le bas donc la destination est décaler vers le bas.

#356 : perfide
#355 : yo-criminel

#510 : chine

# n=3
deplaceYokai(471,999,False)