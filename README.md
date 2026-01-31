# yo-kai-API

Le lien :
https://emerick2.github.io/yo-kai-API/data/jibanyan.json


# Importer les données en JS :
``` js
fetch('https://emerick2.github.io/yo-kai-API/data/jibanyan.json')
.then(response => response.json())
.then(data => {
    console.log("Le nom du Yo-kai est : " + data.nom);
});
```