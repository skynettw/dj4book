import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
alldb = client.list_database_names()
print(alldb)