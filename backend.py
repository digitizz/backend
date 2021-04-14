from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient(
    "mongodb+srv://digitizz:propulsion@bdd.t8p4s.mongodb.net/leads?retryWrites=true&w=majority", tlsAllowInvalidCertificates=True)
db = client["leads"]
collection = db["leads"]

client_pjdb = MongoClient(
    "mongodb://pjdbHamza:pjdbHamzaBouziani@95.216.26.231:27017/pjdb?authSource=pjdb", tlsAllowInvalidCertificates=True)
db_pjdb = client_pjdb["pjdb"]
collection_pjdb = db_pjdb["pjdb"]



@app.route('/<handle>', methods=["GET"])
def home(handle):
    data = collection.find_one({"handle": handle})
    print("DATA", data)
    if data:
        lead = collection_pjdb.find_one({"pj_id": data['pj_id']})
        print("LEAD", lead)
        if lead:
            lead['email'] = lead['emails'][0] if lead['emails'] else None
            lead['phone_number'] = lead['phone_numbers'][0]['number'] if lead['phone_numbers'] else "06 06 06 06 06"
            return render_template('index.html', data=lead)
    return "ERROR"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999, debug=True)
