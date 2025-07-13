import requests
import csv
from pathlib import Path
from .verif import verif_data, verif_file
from .mongo_db import insert_coll
import subprocess
import asyncio
import os


async def recup_insert(username, token, combien):

    url = f"https://api.discogs.com/users/{username}/collection/folders/0/releases"
    headers = {"Authorization": f"Discogs token={token}"}
    params = {"page": 0, "per_page": combien}

    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    temp = ".csv"
    disc_csv_temp = input("le nom ou le chemin de ton csv ou future csv:")  # nom du fichier et ou chemin
    if disc_csv_temp.find(".csv") == -1:
        disc_csv = disc_csv_temp + temp
        print(disc_csv)
        print(type(disc_csv))
    else:
        disc_csv = disc_csv_temp
        print(f"l'entrer du fichier csv est bon,{disc_csv} ")

    for release in data['releases']:

        #Afin de voie le structure de release (ce que nous donne la donnée)
        #print(release)

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

        # présentations des données
        if (len(release['basic_information']['artists'])) == 1:
            print(
                f"L'item {titre} de {artiste} en {formats} sorti en {year} par le label {labels} .Les genres sont {liste_genres} et les styles sont {liste_styles}."
            )
        else:
            print(
                f"L'item {titre} de {liste_artiste} en {formats} sorti en {year} par le label {labels}.Les genres sont {liste_genres} et les styles sont {liste_styles}."
            )

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

        
        file = Path(disc_csv)
        print(file.is_file())

        #si le fichier
        if not file.is_file():
            with open(disc_csv, 'a', newline='') as csvfile:
                fieldnames = [
                    'titre', 'artiste', 'formats', 'formats_discogs', 'year',
                    'labels', 'genres', 'styles'
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                if csvfile.tell() == 0:
                    writer.writeheader()

                writer.writerow(Article)
        else:
            #Verification afin de pouvoir modifier ou ajouter au csv
            if not verif_data(Article, disc_csv):

                with open(disc_csv, 'a', newline='') as csvfile:
                    fieldnames = [
                        'titre', 'artiste', 'formats', 'formats_discogs',
                        'year', 'labels', 'genres', 'styles'
                    ]
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                    if csvfile.tell() == 0:
                        writer.writeheader()

                    writer.writerow(Article)
                    with open('diff.csv', 'a', newline='') as csvfile:
                        fieldnames = [
                            'titre', 'artiste', 'formats', 'formats_discogs',
                            'year', 'labels', 'genres', 'styles'
                        ]
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                        if csvfile.tell() == 0:
                            writer.writeheader()

                        writer.writerow(Article)

    print(
            'les données sont visibles sur le terminal pendant 15 secondes afin que vous puissez visualiser vos données'
        )

    subprocess.run('clear', shell=True)
    verif_file('./discogs_coll.csv','discogs_coll.csv')
    if (os.path.exists('diff.csv') or os.path.exists('remove.csv')):
        insert_coll()
    else:
        print("Il n'y a aucune donnée à incrementer")
        
