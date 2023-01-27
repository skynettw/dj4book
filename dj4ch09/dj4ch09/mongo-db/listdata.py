import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
collections = client["ch08mdb"]["posts"]
records = collections.find()
for rec in records:
    print(rec)
