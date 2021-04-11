from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

@app.route('/<int:id>', methods=["GET"])
def home(id):
    cluster = MongoClient(
        "mongodb+srv://digitizz:propulsion@bdd.t8p4s.mongodb.net/test?retryWrites=true&w=majority", tlsAllowInvalidCertificates=True)
    db = cluster["test"]
    collection = db["test"]
    data = collection.find_one({"_id": id})

    return render_template('index.html', data=data)

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=9999)
