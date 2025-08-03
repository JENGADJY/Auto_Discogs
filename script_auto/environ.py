import os
from pathlib import Path

file =Path('.env')

def create_env_file():
    username = input("Votre nom d'utilisateur discogs:")
    print('https://www.discogs.com/settings/developers')
    token = input(
        "Grâce au lien du dessus , vous pouvez accèder a votre token utilisateur (current token):")
    print(
        "Nous Allons passez à l'étape de l'insertion des données sur mongo_db ")
    print(
        "Vous allez devoir vous créez un compte , puis ensuite créer un cluster gratuit")
    print(
        "N'oubliez surtout pas d'aller dans la section Database access, afin de pouvoir créer un utilisateur qui pourra avoir accès à la base de données")
    print(
        "Et d'allez dans Network accès afin de pouvoir déterminé l'ip avec lequel vous allez intérragir avec mongo db cloud ")
    print(
        "Suite au démarrage du cluster, Vous aurez un onglet 'Connect',Cliquer")
    print("Puis Drivers,Cliquer")
    print(
        "mongodb+srv://<db_username>:<db_password>@xxxx.axfnone.mongodb.net/?retryWrites=true&w=majority&appName=xxxx",
        "Cette ligne similaire apparaitra et vous allez modifier <db_username>:<db_password par votre username et mdp que vous avez selectionné plus tôt dans database accèss.")
    urii = str(input("Coller le ici!:"))
    db_name = str(input("Pour finir le nom de votre db:"))
    filename=".env"
    variables = {
        "MONGO_DB_URL": urii,
        "token_discogs": token,
        "username_discogs": username,
        "MONGO_DBNAME" : db_name,
        "FIRST-TIME": "yes"
    }

    with open(filename, "w") as f:
        for key, value in variables.items():
            f.write(f"{key}={value}\n")

    print(f" Fichier {filename} créé avec succès.")


def modify_env_file(urii,token,username,db_name):
    filename=".env"

    updates = {
        "MONGO_DB_URL": urii,
        "token_discogs": token,
        "username_discogs": username,
        "MONGO_DBNAME" : db_name,
        "FIRST-TIME" : "no"
    }

    # Lire le fichier existant
    env_vars = {}
    if os.path.exists(filename):
        with open(filename, "r") as f:
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    env_vars[key] = value

    # Appliquer les mises à jour
    env_vars.update(updates)

    # Réécrire le fichier
    with open(filename, "w") as f:
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")

    print(f"✅ Fichier {filename} modifié avec succès.")


def update_env_variable(key, value, env_path=".env"):
    lines = []
    found = False

    try:
        with open(env_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            if line.startswith(f"{key}="):
                lines[i] = f"{key}={value}\n"
                found = True
                break

        if not found:
            lines.append(f"{key}={value}\n")

        with open(env_path, "w", encoding="utf-8") as file:
            file.writelines(lines)

    except FileNotFoundError:
        # Si le .env n'existe pas encore
        with open(env_path, "w", encoding="utf-8") as file:
            file.write(f"{key}={value}\n")
            
def change_Mongo_url():
    if not file.is_file():
           print("Vous n'avez pas encore de .env \n Create the . env by choosing the option 3.")
    else:
        choice=str(input("Do you want to change the MONGO_DB_URL ?(yes/no)"))
        match choice :
            case "yes":
                urii=str(input("Veuillez entrer votre MONGO_DB_URL"))
            case "no":
                urii=os.getenv("MONGO_DB_URL")
        return urii

def change_token():
    if not file.is_file():
           print("Vous n'avez pas encore de .env \n Create the . env by choosing the option 3.")
    else:
        choice=str(input("Do you want to change the token ?(yes/no)"))
        match choice :
            case "yes":
                token=str(input("Veuillez entrer votre token"))
            case "no":
                token=os.getenv("token_discogs")
        return token

def change_username():
    if not file.is_file():
           print("Vous n'avez pas encore de .env \n Create the . env by choosing the option 3.")
    else:
        choice=str(input("Do you want to change the user ?(yes/no)"))
        match choice :
            case "yes":
                username=str(input("Veuillez entrer votre Username"))
            case "no":
                username=os.getenv("username_discogs")
        return username

def change_db_name():
    if not file.is_file():
           print("Vous n'avez pas encore de .env \n Create the . env by choosing the option 3.")
    else:
        choice=str(input("Do you want to change the db name ?(yes/no)"))
        match choice :
            case "yes":
                dbname=str(input("Veuillez entrer votre Username"))
            case "no":
                dbname=os.getenv("MONGO_DBNAME")
        return dbname

