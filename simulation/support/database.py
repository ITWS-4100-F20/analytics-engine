import pymongo

MONGO_CONNECTION_STRING="mongodb://itws4500-f20-group5:udJZs6v8a78yVXPspuJs095HjIVhyJQw0myL6jX0pjnggfvwN2NgajyxLdDcNOpzxdZKOGtmJ3Vy6P8ROHOmag==@itws4500-f20-group5.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&maxIdleTimeMS=120000&retrywrites=false&appName=@itws4500-f20-group5@"
client = pymongo.MongoClient(MONGO_CONNECTION_STRING)
print("Client connected to database")