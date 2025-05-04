import csv

def read_roomdb(filepath):
    data = []
    with open(filepath, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(int(row["rb_id"]))
    return data

