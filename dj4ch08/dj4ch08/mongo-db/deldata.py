import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
collections = client["ch08mdb"]["posts"]

records = collections.find()
for rec in records:
    print(rec)
name = input("Please enter the name that you want to delete:")
while name != "":   
    target = collections.delete_one({"name":name})
    records = collections.find()
    for rec in records:
        print(rec)
    name = input("Please enter the name that you want to delete:")
print("Bye!")
    