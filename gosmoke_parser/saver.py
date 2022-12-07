import csv
import json
import os


class Saver():
    """
    This class created for parsers.
    Saved datas to "csv", "json" formats.
    """
    def __init__(self):
        """ Created directory for collected datas. """
        if not os.path.exists('datas'):
            os.mkdir('datas')

    def create_csv_table(self, csv_headers: tuple) -> None:
        """
        Created .csv file with headers.
        :params csv_headers: header tuple.
        """
        with open('datas/table.csv', 'w', encoding='utf-8') as file:
            writer = csv.writer(
                file, dialect='excel', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(csv_headers)

    def save_to_csv(self, fields: tuple) -> None:
        """
        To the file previously created by the method "create_csv_table"
        saved fields with collected datas.
        :params fields: fields tuple.
        """
        with open('datas/table.csv', 'a', encoding='utf-8') as file:
            writer = csv.writer(
                file, dialect='excel', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(fields)

    def save_to_json(self, fields: dict) -> None:
        """
        Saved datas from json format.
        :params fields: dict. explame "{'name': datas}"
        """
        with open('datas/collected_datas.json', 'a', encoding='utf-8') as file:
            json.dump(fields, file, indent=4, ensure_ascii=False)
