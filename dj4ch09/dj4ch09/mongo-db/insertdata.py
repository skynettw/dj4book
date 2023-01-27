import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
collections = client["ch08mdb"]["posts"]

name = input("Name:")
while name != "":
    height = input("Height(cm):")
    weight = input("Weight(kg):")
    collections.insert_one({"name":name, "height":height, "weight":weight})
    name = input("Name:")

records = collections.find()
for rec in records:
    print(rec)
