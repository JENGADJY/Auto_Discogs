import requests
from pathlib import Path
from .verif import verif_data
from .mongo_db import insert_coll
import os
import pandas as ps
from .csv import insert_csv, errors_data, create_file
from dotenv import load_dotenv
from . import environ

load_dotenv()


def recup_insert(username, token, combien):
    first_time = os.getenv("FIRST-TIME")
    disc_csv = 'discogs_coll.csv'
    url = f"https://api.discogs.com/users/{username}/collection/folders/0/releases"
    headers = {"Authorization": f"Discogs token={token}"}
    params = {"page": 0, "per_page": combien}
    file = Path(disc_csv)
    fileDONT = Path('DONT.csv')
    # recuperation du fichier csv au depart afin de faire la verification des elements a supprimer plus tard 
    
    
    if not file.is_file() or file.stat().st_size == 0:
    # fichier n'existe pas ou est vide : créer un fichier CSV avec en-tête
        create_file(disc_csv)

    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    #print(data)
    for release in data['releases']:

        #année de sortie de l'item
        year = release['basic_information']['year']

        #titre de l'item
        titre = release['basic_information']['title']

        #nom de l'artiste ou des artistes
        if (len(release['basic_information']['artists'])) == 1:
            artiste = release['basic_information']['artists'][0]["name"]
        else:
            art_index = release['basic_information']['artists']
            art = 0
            liste_artiste = []
            for art in art_index:
                liste_artiste.append(art["name"])

            #print(liste_artiste)

        #le labels ou les labels de l'item
        labels = release['basic_information']['labels'][0]["name"]

        #format vinyl
        formats_discogs = release['basic_information']['formats'][0]["name"]
        if release['basic_information']['formats'][0][
                "name"] == 'Vinyl' and release['basic_information']['formats'][
                    0]["qty"] == '3':
            formats = '3LP'
            #print(formats)

        if release['basic_information']['formats'][0][
                "name"] == 'Vinyl' and release['basic_information']['formats'][
                    0]["qty"] == '2':
            formats = '2LP'
            #print(formats)

        elif release['basic_information']['formats'][0][
                "name"] == 'Vinyl' and release['basic_information']['formats'][
                    0]["qty"] == '1':
            formats = 'LP'
            #print(formats)

        elif release['basic_information']['formats'][0][
                "name"] == 'CD' or release['basic_information']['formats'][0][
                    "name"] == 'CDr' and release['basic_information'][
                        'formats'][0]["qty"] == '2':
            formats = '2CD'
            #print(formats)

        elif release['basic_information']['formats'][0][
                "name"] == 'CD' or release['basic_information']['formats'][0][
                    "name"] == 'CDr' and release['basic_information'][
                        'formats'][0]["qty"] == '1':
            formats = 'CD'
            #print(formats)

        #else: bug avec le else il ne detecte pas le 3LP
        #    formats='undefined'
        #    #print(formats)

        #genres musicales
        genre_index = release['basic_information']['genres']
        liste_genres = []
        for genre in genre_index:
            liste_genres.append(genre)
        #print(liste_genres)

        #styles musicales
        style_index = release['basic_information']['styles']
        liste_styles = []
        for style in style_index:
            liste_styles.append(style)
        #print(liste_styles)

        Article = {}
        if (len(release['basic_information']['artists'])) == 1:
            Article['titre'] = titre
            Article['artiste'] = artiste
            Article['formats'] = formats
            Article['formats_discogs'] = formats_discogs
            Article['year'] = year
            Article['labels'] = labels
            Article['genres'] = ', '.join(liste_genres)
            Article['styles'] = ', '.join(liste_styles)
        else:
            Article['titre'] = titre
            Article['artiste'] = ', '.join(liste_artiste)
            Article['formats'] = formats
            Article['formats_discogs'] = formats_discogs
            Article['year'] = year
            Article['labels'] = labels
            Article['genres'] = ', '.join(liste_genres)
            Article['styles'] = ', '.join(liste_styles)


        #si le fichier
        if not file.is_file():
            insert_csv(disc_csv,Article)

        else:
            #Verification afin de pouvoir modifier ou ajouter au csv
            if not verif_data(Article, disc_csv):
                if fileDONT.is_file():
                    if first_time =="no": 
                        if errors_data(Article) !=None:
                        #print(errors_data(Article),Article)
                
                            insert_csv(disc_csv,Article)
                            insert_csv('diff.csv',Article)
                    if first_time =="yes": 
                        if errors_data(Article) == None:
                        #print(errors_data(Article),Article)
                
                            insert_csv(disc_csv,Article)
                            insert_csv('diff.csv',Article)

    environ.update_env_variable("FIRST-TIME", "no")                      
    """
    if os.path.exists('./discogs_coll.csv')and os.path.exists('discogs_coll.csv'):
        verif_file('./discogs_coll.csv','discogs_coll.csv')
    """
    if (os.path.exists('diff.csv') ) :
        insert_coll()
    else:
        print("Il n'y a aucune donnée à incrementer")
