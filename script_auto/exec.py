from . import Data ,discogs ,planificateur ,mongo_db,environ
from dotenv import load_dotenv
import os

load_dotenv()

username= os.getenv('username_discogs')
token=os.getenv('token_discogs')

def auto_exe():
    combien = discogs.item_user(username, token)
    Data.recup_insert(username, token, combien)


def script_auto():
  auto_choix=int(input("Que veux-tu faire ?: \n" \
    " 1 -Lancer le script \n" \
    " 2 -Supprimer la db \n" \
    " 3 - Créer le .env \n"
    " 4 - Modifier le .env(si le .env exist)\n " \
    "Veuillez entrer votre entier:")
    )
  match auto_choix:
    case 1:
        planificateur.exc_data()
    case 2:
        mongo_db.delete_db()
        script_auto()
    case 3:
        environ.create_env_file()
        script_auto()
    case 4:
        environ.modify_env_file(
           environ.change_Mongo_url,
           environ.change_token,
           environ.change_username,
           environ.change_db_name,
        )
        script_auto()
    case _ :
      print("un entier pls")
      script_auto()

