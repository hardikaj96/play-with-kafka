from pymongo import MongoClient

# MongoDB configuration
mongo_uri = "mongodb://root:example@mongo:27017"  # Replace with your MongoDB connection details


# Connect to MongoDB

def get_mongodb_client_connection():
    return MongoClient(mongo_uri)
    