import os
import json

DOSSIER = os.path.dirname(os.path.abspath(__file__))

etimologies = {
    "Carpitaine": "Carpitaine est un mot-valise entre « carpe », un poisson d'eau douce, et « capitaine », un grade ou une fonction de commandement. Ce nom fait référence à son statut de chef respecté par les autres poissons.",

    "Triptyk": "Triptyk vient de « triptyque », une œuvre composée de trois panneaux, généralement un panneau central et deux volets latéraux. Ce nom fait référence à ses trois bouches.",

    "Zazel": "Zazel semble être une adaptation du nom « Azazel », une figure démoniaque évoquée dans plusieurs traditions religieuses anciennes. Il est notamment associé au désert dans certaines interprétations. L'origine précise de cette association avec les anciennes croyances cananéennes reste cependant à confirmer.",

    "M. Spioche": "M. Spioche est un mot-valise entre « Monsieur » et « pioche », un outil servant à creuser ou à déterrer des objets. La sonorité du nom rappelle également Spock, le personnage de Star Trek dont l'apparence a inspiré ce Yo-kai.",

    "Indiana Jaws": "Indiana Jaws est un mot-valise entre « Indiana Jones », le célèbre aventurier de fiction, et « Jaws », le titre original du film Les Dents de la mer. « Jaws » signifie également « mâchoires » en anglais, en référence à son apparence de requin.",

    "Nyansès II": "Nyansès II est un mot-valise entre « nyan », l'onomatopée japonaise représentant le miaulement d'un chat, et « Ramsès II », un célèbre pharaon égyptien de la XIXe dynastie. Son nom japonais, « Neko II », signifie « Chat II » et peut également évoquer Nékao II (Necho II), un pharaon égyptien. Attention : « nisei » ne signifie pas « pharaon » en japonais.",

    "Phémniscian": "Phémniscian est un mot-valise entre « phénix », un oiseau légendaire capable de renaître de ses cendres, et « Domniscian », le Yo-kai dont il est la transformation.",

    "Barbrakai": "Barbrakai semble être un mot-valise entre « Barbokai », le Yo-kai dont il est une variante, et « bras », en référence à son apparence ou à sa force physique. Cette construction reste une hypothèse, car l'origine exacte du nom français n'est pas confirmée.",

    "Boulet grillé": "Boulet grillé reprend le nom « Boulet frit », auquel est substitué « grillé », qui désigne un aliment cuit directement à la chaleur. Ce changement fait référence à son crime lié à ses sous-vêtements.",

    "Épigepa": "Épigepa reprend le nom « Épigerien » en le transformant en « j'y pige pas », une expression familière qui signifie ne rien comprendre. La terminaison « pa » fait ainsi référence à la négation « pas ».",

    "Eddylettante": "Eddylettante est un mot-valise entre « Eddylapid », le Yo-kai dont il est une variante, et « dilettante », une personne qui pratique une activité de manière peu sérieuse ou sans véritable investissement. Ce nom fait référence à son manque d'implication dans le travail de groupe.",

    "Beurk O'Max": "Beurk O'Max reprend le nom « Big O'Max », auquel est ajoutée l'interjection « beurk ! », qui exprime le dégoût. Ce nom fait référence à son comportement particulièrement répugnant.",

    "Déloyau Ier": "Déloyau Ier est un mot-valise entre « déloyal », qui qualifie une personne qui ne respecte pas les règles de loyauté, et « Aloyau Ier », le Yo-kai dont il est une variante. Le nom conserve la référence royale de son prédécesseur.",

    "TuPakap": "TuPakap est un mot-valise entre « TuKappa », le Yo-kai dont il est une variante, et l'expression « t'es pas cap », utilisée pour provoquer quelqu'un en mettant en doute sa capacité à accomplir quelque chose.",

    "Cracrassiella": "Cracrassiella reprend le nom « Crassiella », auquel est ajouté « cracra », un terme familier qui signifie sale ou malpropre. Ce nom fait référence à son comportement malicieux.",

    "Outrecuidansss": "Outrecuidansss est un mot-valise entre « Outransss », le Yo-kai dont il est une variante, et « outrecuidance », qui désigne une attitude excessive de présomption, d'arrogance ou de prétention. La terminaison « sss » évoque le sifflement d'un serpent.",

    "Soidisanss": "Soidisanss est un mot-valise entre « Médisansss », le Yo-kai dont il est une variante, et « soi-disant », une expression utilisée pour présenter quelque chose comme prétendu ou supposé. La terminaison « sss » évoque le sifflement d'un serpent.",

    "Grommella": "Grommella est un mot-valise entre « Brumella », le Yo-kai dont elle est une variante, et « grommeler », un verbe qui signifie exprimer son mécontentement en marmonnant.",

    "Sabroclair": "Sabroclair est un mot-valise entre « sabre », une arme blanche dont la lame est généralement tranchante sur un seul côté, et l'expression « au clair », utilisée notamment dans « tirer son sabre au clair », qui signifie sortir son arme de son fourreau. Son nom japonais, « Bōrei Mushei », signifie « samouraï fantôme ». Son nom anglais, « Phantasmurai », combine « phantasm » (fantasme ou apparition) et « samurai » (samouraï).",

    "Inamygal": "Inamygal est un mot-valise entre « inamical », qui qualifie une personne peu sympathique ou hostile, et « mygale », une grande araignée. Ce nom fait référence à son apparence et à son caractère prédateur.",

    "Dr Jobard": "Dr Jobard associe « Dr », l'abréviation de « docteur », et « Jobard », un terme familier qui désigne une personne naïve ou crédule. Ce dernier mot est également à l'origine de « barjo », son équivalent en verlan, qui signifie fou ou extravagant. Ce nom fait référence à son caractère de savant fou.",

    "Firmain": "Firmain est un mot-valise entre le prénom « Firmin » et « main », en référence à son corps constitué de nombreuses mains.",

    "Fatracteur": "Fatracteur est un mot-valise entre « fatras », qui désigne un amas désordonné d'objets, et « tracteur », un véhicule capable de tracter ou de tirer de lourdes charges. Ce nom fait référence à son corps constitué de débris et de ferraille. Son nom anglais, « Junkernaut », combine « junk » (ordures ou objets inutiles) et « juggernaut » (une force immense et destructrice). Son nom espagnol, « Chatárrenstein », combine « chatarra » (ferraille) et « Frankenstein ».",

    "Supermanager": "Supermanager associe « super », qui évoque quelque chose d'extraordinaire ou de supérieur, et « manager », un terme anglais désignant une personne chargée de gérer une entreprise ou une équipe. Le mot « super » peut également faire référence au supermarché dont il est le gérant.",

    "Minustrel": "Minustrel est un mot-valise entre « minuit », le moment où commence un nouveau jour, et « ménestrel », un musicien ou poète itinérant du Moyen Âge. Ce nom fait référence à son apparence de flûtiste et à son pouvoir qui pousse les gens à abandonner leurs obligations.",

    "King Keskler": "King Keskler associe « King », qui signifie « roi » en anglais, et « caisse claire », un instrument de percussion également appelé tambour de caisse claire. Le mot « Keskler » reproduit phonétiquement une partie de l'expression « caisse claire ». Ce nom fait référence à son talent de percussionniste et à son surnom de roi de la scène musicale.",

    "Yo-kaiju": "Yo-kaiju est un mot-valise entre « Yo-kai » et « kaiju », un terme japonais désignant un monstre géant, notamment dans le cinéma japonais. Le nom fait référence à sa taille gigantesque.",

    "Dodorothée": "Dodorothée est un mot-valise entre « dodo », un terme enfantin qui désigne le sommeil, et le prénom féminin « Dorothée ». Ce nom évoque à la fois son prénom et son rôle de mère.",

    "Yopple-bot": "Yopple-bot est un mot-valise entre « Yopple », le nom de l'entreprise fictive qui l'a développé, et « bot », une abréviation du mot anglais « robot ». Yopple peut également rappeler Apple, l'entreprise technologique américaine, mais cette origine du nom de la société fictive reste une interprétation.",

    "Hydreux": "Hydreux est un mot-valise entre « hydre », une créature mythologique souvent représentée comme un serpent ou un dragon possédant plusieurs têtes, et « yeux », les organes de la vision. Ce nom fait référence à ses nombreux yeux et à son apparence de créature monstrueuse.",

    "Styx VI": "Styx VI associe « Styx », le nom d'une Océanide de la mythologie grecque qui personnifie également le fleuve séparant le monde des vivants de celui des morts, et « VI », le chiffre six en numération romaine. La version anglaise, « Styx Mk. VI », suggère également une référence à un modèle ou une série de navires.",

    "Maximain": "Maximain est un mot-valise entre « maxi », une abréviation de « maximum » qui évoque une quantité ou une taille très importante, et « main », en référence aux nombreuses mains de ce Yo-kai.",

    "Nébulor": "L'étymologie française de « Nébulor » n'est pas clairement établie. Son nom anglais, « Clipso », vient d'« eclipse » (éclipse). Son nom japonais, « Tsukikage Nyūdō », peut être traduit par « moine chauve de l'ombre de la lune » ou « moine chauve au clair de lune ». Il est préférable de conserver ces deux références plutôt que d'inventer une décomposition certaine du nom français.",

    "Pr Létripe": "Pr Létripe associe « Pr », l'abréviation de « professeur », et « les tripes », qui désignent les intestins ou les entrailles. La prononciation du nom rappelle directement l'expression « professeur les tripes ».",

    "Potofeu": "Potofeu vient de « pot-au-feu », un plat traditionnel français composé de viande et de légumes cuits dans un bouillon. Ce nom fait référence à son apparence de récipient de cuisson.",

    "McKraken": "Le nom complet de ce Yo-kai est « Calamus McKraken ». « Calamus » vient de « calamar », un mollusque marin, tandis que « McKraken » fait référence au « kraken », un monstre marin légendaire représenté sous la forme d'une créature gigantesque aux nombreux tentacules.",

    "Don Morleone": "Don Morleone vient de « Don Corleone », le célèbre personnage de fiction du roman et du film Le Parrain. « Don » est un titre honorifique utilisé notamment pour désigner un chef de la mafia. Son nom japonais, « Gogogo Godfather », associe « Godfather » (parrain) et « go » (五), qui signifie cinq en japonais. La répétition du chiffre cinq évoque les 555 années durant lesquelles il a été exilé, ainsi que les 555 étages de sa tour. « Gogogo » peut également évoquer une onomatopée japonaise exprimant une atmosphère menaçante. Son nom anglais, « The Ghoulfather », combine « ghoul » (goule) et « Godfather ». Enfin, « Don Spiration » associe « Don » et « conspiracy » (conspiration).",

    "Extrabuki": "Extrabuki est un mot-valise entre « extra », qui désigne quelque chose de supplémentaire ou d'exceptionnel, et « kabuki », une forme traditionnelle de théâtre japonais. Ce nom fait référence à son talent de comédien.",

    "Magnustrel": "L'origine française de Magnustrel n'est pas clairement documentée. Son nom anglais, « Slackolyte », est un mot-valise entre « slack », qui signifie notamment relâcher ou diminuer l'intensité, et « acolyte », un terme désignant un disciple ou un compagnon. Ce nom fait référence à son rôle d'acolyte et à son comportement.",

    "Domniscian": "Domniscian pourrait être un mot-valise entre « dominant », qui désigne une personne ou une entité qui exerce une autorité supérieure, et « omniscient », qui qualifie une personne qui sait tout. Cette origine correspond à ses pouvoirs extraordinaires, mais reste une hypothèse. Son nom japonais fait notamment référence à Akihiro Hino, le fondateur et président de LEVEL-5, et au mot « kami », qui signifie « dieu » en japonais.",

    "Domniscian 2.0": "Domniscian 2.0 reprend le nom de Domniscian, auquel est ajouté « 2.0 », une notation couramment utilisée en informatique pour désigner une nouvelle version ou une évolution d'un produit. Le nom conserve les références possibles à « dominant » et « omniscient ».",

    "Rôdin": "Rôdin vient du verbe « rôder », qui signifie se déplacer furtivement, souvent dans un lieu de manière inquiétante ou suspecte. Ce nom fait référence à son apparition derrière les personnes qui traversent les ruelles sombres. Son nom anglais, « Skulk », possède un sens proche et signifie se déplacer furtivement ou en secret. Son nom japonais, « Bishagatsuku », fait référence au Yo-kai Bishagatsuku du folklore japonais.",

    "Gargaros": "Gargaros pourrait être un mot-valise entre « gargouille », une sculpture souvent représentée sous une forme monstrueuse, et « Gargantua », un géant issu de l'œuvre de François Rabelais. Ces deux rapprochements sont possibles, mais il n'est pas établi avec certitude que les créateurs aient retenu l'un plutôt que l'autre.",

    "Komak": "Komak associe « Koma », provenant de « komainu », les statues de chiens-lions qui gardent les sanctuaires japonais, et « Mac ». Cette seconde partie est parfois expliquée comme une référence à un stéréotype de personnages néerlandais musclés. Attention toutefois : « Mac » est historiquement un préfixe patronymique gaélique signifiant « fils de », et non un préfixe typiquement néerlandais. Cette interprétation reste donc incertaine.",

    "Robonyan 28": "Robonyan 28 reprend le nom de « Robonyan », un mot-valise entre « robot » et « nyan », l'onomatopée japonaise représentant le miaulement d'un chat. Le chiffre 28 indique qu'il s'agit de sa vingt-huitième version. Il constitue également une référence probable à Tetsujin 28-go, un célèbre robot géant du manga et de l'animation japonaise.",

    "Don Dorleone": "Don Dorleone est un mot-valise entre « Don Morleone », le Yo-kai dont il est issu, et « or », le métal précieux. Son nom fait référence à sa transformation dorée et à son obsession pour les richesses.",

    "Ténorque": "Ténorque est un mot-valise entre « ténor », une voix masculine située entre le baryton et le contre-ténor, et « orque », un grand cétacé carnivore également appelé épaulard. Ce nom fait référence à son apparence de baleine et à son puissant rugissement.",

    "Morquis": "Morquis est un mot-valise entre « orque », un grand cétacé marin, et « marquis », un titre de noblesse situé traditionnellement entre le comte et le duc. Son nom anglais, « Whaleman », combine « whale » (baleine) et « man » (homme).",

    "Roi Shogun": "Roi Shogun associe « roi », qui désigne un souverain, et « shogun », le titre du dirigeant militaire suprême du Japon féodal. Son nom japonais, « Bushi-ō », signifie « roi des guerriers », car « bushi » désigne un guerrier japonais et « ō » signifie « roi ».",

    "Tyragofeu": "Tyragofeu est un mot-valise formé à partir de trois Yo-kai : TYRAgédie, PoGOrille et FEUlion. Chaque partie du nom reprend une portion du nom des trois créatures qui composent cette fusion.",

    "Robonyan 3000": "Robonyan 3000 reprend le nom de « Robonyan », auquel est ajouté le nombre 3000 pour indiquer une version beaucoup plus avancée de ses modèles précédents, notamment Robonyan 28. Ce nombre évoque une nouvelle génération de robot.",

    "Blingos": "Blingos est un mot-valise entre « bling-bling », une expression familière désignant des bijoux ou des accessoires particulièrement voyants et luxueux, et « os », en référence à son apparence de squelette.",

    "Bogos": "Bogos est un mot-valise entre « beau gosse », une expression familière désignant un homme séduisant, et « os », en référence à son apparence de squelette. La lettre « g » permet de faire apparaître le son de « gosse » dans le nom.",

    "Cycloptique": "Cycloptique est un mot-valise entre « cyclope », une créature de la mythologie grecque qui ne possède qu'un seul œil, et « optique », un terme relatif à la vision et à la lumière.",

    "Taprice": "Taprice est un mot-valise entre « taper », le verbe qui signifie frapper, et « caprice », un désir soudain ou une exigence arbitraire. Son nom japonais, « Derukuitataki », fait référence au proverbe « le clou qui dépasse est enfoncé », qui signifie que les personnes qui se distinguent des autres sont souvent remises à leur place. Son nom anglais, « Mallice », combine « mallet » (maillet) et « malice » (méchanceté).",

    "Pattes Rouges": "Pattes Rouges associe « pattes », en référence aux membres d'un animal, notamment ceux d'un chat, et « rouges », la couleur de ses pattes. Son nom décrit directement son apparence.",

    "Griffes Dorées": "Griffes Dorées associe « griffes », les ongles pointus et recourbés de certains animaux, et « dorées », qui désigne une couleur semblable à celle de l'or. Son nom fait référence à son apparence dorée.",

    "Or Tourbillonnant": "Or Tourbillonnant associe « or », un métal précieux, et « Omai Tourbillonnant », le Yo-kai dont il est une forme améliorée. Le nom fait référence à son apparence dorée et à son pouvoir lumineux.",

    "Zazelmar": "Zazelmar est un mot-valise entre « Zazel », le Yo-kai dont il est issu, et « cauchemar », un rêve effrayant. Ce nom fait référence à sa nature maléfique et à son apparence terrifiante.",

    "Emperose": "Emperose est un mot-valise entre « empereur », un souverain qui gouverne un empire, et « rose », la couleur de son corps. Son nom évoque son apparence de souverain entièrement rose.",

    "Ducanin": "Ducanin est un mot-valise entre « duc », un titre de noblesse, et « canin », un adjectif relatif aux chiens. Ce nom fait référence à son apparence canine et à son rôle de protecteur de Zazel.",

    "Ducfélin": "Ducfélin est un mot-valise entre « duc », un titre de noblesse, et « félin », un adjectif relatif aux chats et aux animaux de la famille des félins. Ce nom fait référence à son apparence de chat et à son rôle de protecteur de Zazel."
}

for fichier in os.listdir(DOSSIER):
    if not fichier.endswith(".json"):
        continue

    chemin = os.path.join(DOSSIER, fichier)

    with open(chemin, "r", encoding="utf-8") as f:
        donnees = json.load(f)

    modifications = 0

    yokais = donnees if isinstance(donnees, list) else [donnees]

    for yokai in yokais:
        nom = yokai.get("Nom")

        if nom in etimologies:
            yokai["étimologie"] = etimologies[nom]
            modifications += 1

    if modifications > 0:
        with open(chemin, "w", encoding="utf-8") as f:
            json.dump(donnees, f, ensure_ascii=False, indent=2)

        print(f"{fichier} : {modifications} étymologie(s) ajoutée(s).")

print("\nTerminé !")