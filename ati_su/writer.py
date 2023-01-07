import csv
import os


class Saver:
    def __init__(self, csv_headers):
        if not os.path.exists('data'):
            os.mkdir('data')

        with open('data/table.csv', 'w', encoding='utf-8') as file:
            writer = csv.writer(
                file, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(csv_headers)

    @staticmethod
    def save_in_csv(fields):
        with open('data/table.csv', 'a', encoding='utf-8') as file:
            writer = csv.writer(
                file, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(fields)
