from pymongo import MongoClient
import json
import csv


client = MongoClient("mongodb://pjdbHamza:pjdbHamzaBouziani@95.216.26.231:27017/pjdb?authSource=pjdb", tlsAllowInvalidCertificates=True)
db = client["test"]
collection = db['pjdb']

def mongo_export_to_file():
    today = datetime.today()
    today = today.strftime("%m-%d-%Y")
    _, _, instance_col = set_db()
    # make an API call to the MongoDB server
    collection = instance_col.find()
    if collection.count() == 0:
        return

    fieldnames = list(collection[0].keys())
    fieldnames.remove('_id')

    # compute the output file directory and name
    output_dir = os.path.join(
        '..', '..', 'plombiers', 'aws_instance_list', 'csv', '')
    output_file = os.path.join(
        output_dir, 'plombiers' + today + '.csv')
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(
            csvfile, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(collection)
