import csv
import pandas as ps

def insert_csv(disc_csv,Article):
    with open(disc_csv,'a', newline='', encoding='cp1252', errors='replace') as csvfile:
                fieldnames = [
                    'titre', 'artiste', 'formats', 'formats_discogs', 'year',
                    'labels', 'genres', 'styles'
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                if csvfile.tell() == 0:
                    writer.writeheader()

                writer.writerow(Article)

def errors_data(Article):
        error_items=ps.read_csv('DONT.csv', sep=",", on_bad_lines='warn', encoding='cp1252')
        for row in error_items:
            if Article == row:
                break

def create_file(disc_csv):
      with open(disc_csv, 'w', newline='', encoding='cp1252') as csvfile:
            fieldnames = [
            'titre', 'artiste', 'formats', 'formats_discogs', 'year',
            'labels', 'genres', 'styles'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()