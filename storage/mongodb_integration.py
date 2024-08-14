from pymongo import MongoClient

def store_metadata_in_mongodb(data):
    client = MongoClient('mongodb://mongodb:27017/')
    db = client['lmm_upgrade']
    collection = db['metadata']
    collection.insert_one(data)
    print("Data successfully stored in MongoDB")

if __name__ == "__main__":
    example_data = {'title': 'Sample Title', 'content': 'Sample content'}
    store_metadata_in_mongodb(example_data)
