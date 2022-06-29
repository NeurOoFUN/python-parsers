import csv
import json
import os


class Saver:
    def __init__(self):
        """ Created directory for collected datas. """
        if not os.path.exists('datas'):
            os.mkdir('datas')

    @staticmethod
    def create_csv_table(csv_headers: tuple):
        with open('datas/table.csv', 'w', encoding='utf-8') as file:
            writer = csv.writer(
                file, dialect='excel', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(csv_headers)

    @staticmethod
    def save_to_csv(fields: tuple):
        with open('datas/table.csv', 'a', encoding='utf-8') as file:
            writer = csv.writer(
                file, dialect='excel', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(fields)

    @staticmethod
    def save_to_json(fields: dict):
        with open('datas/collected_datas.json', 'a', encoding='utf-8') as file:
            json.dump(fields, file, indent=4, ensure_ascii=False)
