from pymongo import MongoClient
import json
import csv
import random

client = MongoClient(
    "mongodb+srv://digitizz:propulsion@bdd.t8p4s.mongodb.net/leads?retryWrites=true&w=majority", tlsAllowInvalidCertificates=True)
db = client["leads"]
collection = db["leads"]

client_pjdb = MongoClient(
    "mongodb://pjdbHamza:pjdbHamzaBouziani@95.216.26.231:27017/pjdb?authSource=pjdb", tlsAllowInvalidCertificates=True)
db_pjdb = client_pjdb["pjdb"]
collection_pjdb = db_pjdb["pjdb"]

def mongo_export_to_file(label):
    leads = collection_pjdb.find({"activities.label": label, "emails": {"$ne": []}})

    # compute the output file directory and name
    with open(f"{label}.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["name","handle", "pj_id", "city", "email"])
        for lead in leads:
            print("lead", lead)
            email = lead['emails'][0]
            city = lead['address']['city'].lower() if lead['address']['city'] else "paris"
            handle = lead['name'].lower().replace(" ", "-")
            try:
                collection.insert_one({
                    "handle": handle,
                    "pj_id": lead['pj_id']
                })
            except Exception as e:
                message = getattr(e, 'message', repr(e))
                print("EXCEPTION", message)
                if 'E11000 duplicate key error' in message:
                    random_int = random.randint(100, 1000)
                    handle += f"-{random_int}"
                    collection.insert_one({
                        "handle": handle,
                        "pj_id": lead['pj_id']
                    })

            writer.writerow([lead['name'], handle, lead['pj_id'], city, email])

mongo_export_to_file("PLOMBIERS")