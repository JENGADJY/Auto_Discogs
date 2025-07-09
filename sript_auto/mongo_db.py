from pymongo.mongo_client import MongoClient
import pandas as ps
from dotenv import load_dotenv
import os
import path


load_dotenv()

urii=os.getenv('MONGO_DB_URL')


def insert_coll():
    user_client = MongoClient(urii)
    user_db = user_client['lmsbdata']
    user_col = user_db["DISCOGS_items"]

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
                filter_to_delete = {
                '$or': [
                {'titre': doc['titre'], 'artiste': doc['artiste'], 'formats': doc['formats']}
                for doc in df_remove.to_dict('records')
                ]
            }
            delete_result = user_col.delete_many(filter_to_delete)
            print('Parfait, les données ont bient été recupérée,voici les nouvelles données entrer:')
            print(df_remove)
            #suppresion afin de pouvoir supprrimé les elements supplémentaires qui vont arrivées par la suite
            os.remove('remove.csv')


