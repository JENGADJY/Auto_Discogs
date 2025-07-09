from . import fonction
from . import discogs
from dotenv import load_dotenv
import os


load_dotenv()

username= os.getenv('username_discogs')
token=os.getenv('token_discogs')

def auto_exe():
    combien = discogs.item_user(username, token)
    fonction.recup_insert(username, token, combien)


