from pymongo.mongo_client import MongoClient
import pandas as ps
import os
import csv


def insert_coll():
    #Ajouts des nouveaux elements via diff meme si nouveau fichier , il sera supprimé

    print(
        "Nous Allons passez à l'étape de l'insertion des données sur mongo_db "
    )
    print(
        "Vous allez devoir vous créez un compte , puis ensuite créer un cluster gratuit"
    )
    print(
        "N'oubliez surtout pas d'aller dans la section Database access, afin de pouvoir créer un utilisateur qui pourra avoir accès à la base de données"
    )
    print(
        "Et d'allez dans Network accès afin de pouvoir déterminé l'ip avec lequel vous allez intérragir avec mongo db cloud "
    )
    print(
        "Suite au démarrage du cluster, Vous aurez un onglet 'Connect',Cliquer"
    )
    print("Puis Drivers,Cliquer")
    print(
        "mongodb+srv://<db_username>:<db_password>@xxxx.axfnone.mongodb.net/?retryWrites=true&w=majority&appName=xxxx",
        "Cette ligne similaire apparaitra et vous allez modifier <db_username>:<db_password par votre username et mdp que vous avez selectionné plus tôt dans database accèss."
    )
    urii = str(input("Coller le ici!:"))
    user_client = MongoClient(urii)
    db_name = str(input("Comment voulez-vous appellé votre db :"))

    df = ps.read_csv('diff.csv')
    user_db = user_client[db_name]
    user_col = user_db["DISCOGS_items"]
    x = user_col.insert_many(df.to_dict('records'))

    print(
        'Parfait, les données ont bient été recupérée,voici les nouvelles données entrer:'
    )
    print(df)

    #suppresion afin de pouvoir ajouté les elements supplémentaires qui vont arrivées par la suite
    os.remove('diff.csv')
    print('Diff.csv a été supprimé')
