a faire :
creer un env pour le client comme ca il pourra ensuite devenir proprio .(ou sinon interface web + server comme ca c'est moi qui stocke les donnéess des gens .)
interface et enregistrement utilisateur
PUIS REDIRECTION POWERBI

Pour demarrer le script:

```bash
    git clone https://github.com/JENGADJY/Auto_Discogs.git
    cd Auto_Discogs/
    pip install -r requirements.txt
    python3 main.py

```

Tout d'abord client et
si vous avez soit deja mit vos info dans le .env ou deja tester en tant que client , il faudra aller en tant que proprio

pour l'automatisation:

```bash
 MONGO_DB_URL=
 username_discogs=
 Discogs_token=
```

Si vous voullez lire le programme depuis un fichier externe voici une base pour un autre main.py:

```python
    import asyncio
    from Auto_Discogs import main as Auto_Discogs_main


    def main():
        Auto_Discogs_main.main()


    if __name__ == '__main__':
        main()

```

Si vous voulez l'executez sur replit , copier les fichiers qui sont dans le replit/



https://stackoverflow.com/questions/63484742/how-to-write-in-env-file-from-python-code ///// plus tard
