import os
from .fonction import recup_insert
from dotenv import load_dotenv
import asyncio

import pymongo

load_dotenv()
myclient = pymongo.MongoClient(os.getenv('MONGO_KEY'))


async def client_execut():

    username = input("Votre nom d'utilisateur discogs:")
    print('https://www.discogs.com/settings/developers')
    token = input(
        "Grâce au lien du dessus , vous pouvez accèder a votre token utilisateur (current token):"
    )
    nombre = int(input("Pour finir vous avez combien d'item ?:"))

    if type(username) is str and type(token) is str and type(nombre) is int:
        await recup_insert(username, token, nombre)
    else:
        print(
            f"Il faut que l'username soit une chaine de charactère(str).Voici ce que l'on reçoit {username} et voici le type:{type(username)}"
        )
        print(
            f"Il faut que token soit aussi une chaine de charactère(str).Voici ce que l'on reçoit {token} et voici le type:{type(token)}"
        )
        print(
            f"Et pour finir que le nombre d'item soit en entier (int).Voici ce que l'on reçoit {nombre} et voici le type:{type(nombre)}"
        )
        print("Veuillez re-rentrer vos coordonnées ")
        await client_execut()


