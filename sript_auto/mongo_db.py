from pymongo.mongo_client import MongoClient
import pandas as ps
from dotenv import load_dotenv
import os
import path


load_dotenv()

urii=os.getenv('MONGO_DB_URL')
client_mongo=os.getenv('MONGO_DBNAME')


user_client = MongoClient(urii)
user_db = user_client[client_mongo]
user_col = user_db["DISCOGS_items"]

def insert_coll():

    if os.path.exists('diff.csv'):
        with open('diff.csv', encoding='utf-8', errors='ignore') as f:
            df_enter = ps.read_csv(f, engine='python')
                
            if not df_enter.empty:
                add = user_col.insert_many(df_enter.to_dict('records'))
                print('Parfait, les données ont bient été recupérée,voici les nouvelles données entrer:')
                print(df_enter)
                #suppresion afin de pouvoir ajouté les elements supplémentaires qui vont arrivées par la suite
        os.remove('diff.csv')
        print('Diff.csv a été supprimé')

    if os.path.exists('remove.csv'):
        with open ('remove.csv',encoding='utf-8', errors='ignore') as f:
            df_remove = ps.read_csv(f, engine='python')

            if not df_remove.empty:
                required_keys = ['titre', 'artiste', 'formats', 'formats_discogs', 'year', 'labels', 'genres', 'styles']
                filter_to_delete = {
                    '$or': []
                }
    
                for doc in df_remove.to_dict('records'):
                    if all(key in doc and doc[key] is not None for key in required_keys):
                        filter_to_delete['$or'].append({key: doc[key] for key in required_keys})
    
                if filter_to_delete['$or']:
                    delete_result = user_col.delete_many(filter_to_delete)
                    print('Suppression effectuée avec succès pour ces documents :')
                    print(df_remove)
                else:
                    print("Aucun document valide à supprimer.")
        os.remove('remove.csv')

def delete_db():
    print(f"{user_col} has been deleted")
    user_col.drop()
    os.remove('discogs_coll.csv')