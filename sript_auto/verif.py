import pandas as pd
import csv


def verif_data(Article, disc_csv):

    df = pd.read_csv(disc_csv , sep=",", on_bad_lines='warn', encoding='ISO-8859-1')

    if df.empty == True:
        exists = False
        return exists

    else:

        verif = []
        with open(disc_csv, newline='', encoding='ISO-8859-1') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                verif.append(row)

            # juste verifier si les attributs de l'article corespondent 
            exists = False
            for row in verif:
                if Article['titre'] == row['titre'] and Article['artiste'] == row['artiste'] and Article['formats'] == row['formats']  :
                    exists = True
                    print(f"{Article['titre']} est deja dans le csv")
                    return exists
                    
            return exists


def verif_file(csv1,csv2,csv3=None):
    #option 1 : verif entre les fichiers discogs_coll.csv afin d'eviter les confusions et de les synchro
    df1 = pd.read_csv(csv1 , sep=",", on_bad_lines='warn', encoding='ISO-8859-1')
    df2 = pd.read_csv(csv2 , sep=",", on_bad_lines='warn', encoding='ISO-8859-1')

    list1 = df1.to_dict('records')
    list2 = df2.to_dict('records')
    
    rows_to_add_to_csv2 = [row for row in list1 if row not in list2]
    rows_to_add_to_csv1 = [row for row in list2 if row not in list1] 

    if csv3 is not None :
        list3 = csv3.to_dict('records')

        rows_to_delete_in_csv1= [row for row in list3 if not row in list1]
        rows_to_delete_in_csv2= [row for row in list3 if not row in list2]

        if rows_to_delete_in_csv1:
            fieldnames = ['titre', 'artiste', 'formats', 'formats_discogs', 'year', 'labels', 'genres', 'styles']
            with open('remove.csv', 'a', newline='', encoding='ISO-8859-1',errors='replace') as csvfile:  
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerows(rows_to_delete_in_csv1)
                print(f"Added {len(rows_to_delete_in_csv1)} va etre supprimé mais pour l'instant est dans delete")


        if rows_to_delete_in_csv2:
            fieldnames = ['titre', 'artiste', 'formats', 'formats_discogs', 'year', 'labels', 'genres', 'styles']
            with open('remove.csv', 'a', newline='', encoding='ISO-8859-1',errors='replace') as csvfile:  
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerows(rows_to_delete_in_csv2)
                print(f"Added {len(rows_to_delete_in_csv2)} va etre supprimé mais pour l'instant est dans delete")

        fieldnames = ['titre', 'artiste', 'formats', 'formats_discogs', 'year', 'labels', 'genres', 'styles']

        df1_cleaned = df1.merge(csv3[fieldnames], on=fieldnames, how='left', indicator=True)
        df1_cleaned = df1_cleaned[df1_cleaned['_merge'] == 'left_only'].drop(columns=['_merge'])
        df1_cleaned.to_csv(csv1, index=False, encoding='ISO-8859-1')
        print(f"{len(df1) - len(df1_cleaned)} ligne(s) supprimée(s) de {csv1}")

        df2_cleaned = df2.merge(csv3[fieldnames], on=fieldnames, how='left', indicator=True)
        df2_cleaned = df2_cleaned[df2_cleaned['_merge'] == 'left_only'].drop(columns=['_merge'])
        df2_cleaned.to_csv(csv2, index=False, encoding='ISO-8859-1')
        print(f"{len(df2) - len(df2_cleaned)} ligne(s) supprimée(s) de {csv2}")
   

    if rows_to_add_to_csv2:
        fieldnames = ['titre', 'artiste', 'formats', 'formats_discogs', 'year', 'labels', 'genres', 'styles']
        with open(csv2, 'a', newline='', encoding='ISO-8859-1') as csvfile: 
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writerows(rows_to_add_to_csv2)
            print(f"Added {len(rows_to_add_to_csv2)} rows from {csv1} to {csv2}")

    if rows_to_add_to_csv1:
        fieldnames = ['titre', 'artiste', 'formats', 'formats_discogs', 'year', 'labels', 'genres', 'styles']
        with open(csv1, 'a', newline='', encoding='ISO-8859-1') as csvfile:  
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerows(rows_to_add_to_csv1)
            print(f"Added {len(rows_to_add_to_csv1)} rows from {csv2} to {csv1}")

    # Creation d'un fichier delete avec qui supprimer dans discogs_coll et mongodb           

