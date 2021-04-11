from pymongo import MongoClient
import pandas

# build a new client instance of MongoClient
mongo_client = MongoClient(
    "mongodb://pjdbHamza:pjdbHamzaBouziani@95.216.26.231:27017/pjdb?authSource=pjdb")

# create new database and collection instance
db = mongo_client.some_database
col = db.some_collection

# make an API call to the MongoDB server
cursor = col.find()

# extract the list of documents from cursor obj
mongo_docs = list(cursor)

# restrict the number of docs to export
mongo_docs = mongo_docs[:50]  # slice the list
print("total docs:", len(mongo_docs))

# create an empty DataFrame for storing documents
docs = pandas.DataFrame(columns=[])

# iterate over the list of MongoDB dict documents
for num, doc in enumerate(mongo_docs):

    # convert ObjectId() to str
    doc["_id"] = str(doc["_id"])

# get document _id from dict
doc_id = doc["_id"]

# create a Series obj from the MongoDB dict
series_obj = pandas.Series(doc, name=doc_id)

# append the MongoDB Series obj to the DataFrame obj
docs = docs.append(series_obj)

# only print every 10th document
if num % 10 == 0:
    print(type(doc))
    print(type(doc["_id"]))
    print(num, "--", doc, "\n")

print("\nexporting Pandas objects to different file types.")
print("DataFrame len:", len(docs))

# export MongoDB documents to a CSV file
docs.to_csv("plombier.csv", ",")  # CSV delimited by commas

# export MongoDB documents to CSV
csv_export = docs.to_csv(sep=",")  # CSV delimited by commas
print("\nCSV data:", csv_export)

print("\n\ntime elapsed:", time.time()-start_time)
