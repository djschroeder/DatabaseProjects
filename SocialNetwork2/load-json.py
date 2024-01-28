import pymongo
import json
import sys


def connect_to_mongodb(port):
    """ Connect to the MongoDB server on the given port. """
    try:
        client = pymongo.MongoClient('localhost', int(port))
        return client
    except pymongo.errors.ConnectionFailure as e:
        print(f"Could not connect to MongoDB: {e}")
        sys.exit(1)


def create_database_and_collection(client):
    """ Create '291db' database and 'tweets' collection. Drop the collection if it already exists. """
    db = client['291db']
    if 'tweets' in db.list_collection_names():
        db['tweets'].drop()
    collection = db['tweets']
    return collection


def load_json_data(file_name, collection):
    """ Load JSON data from file and insert into the collection in batches. """
    try:
        with open(file_name, 'r') as file:
            batch = []
            for line in file:
                try:
                    tweet = json.loads(line)
                    batch.append(tweet)
                    if len(batch) >= 1000:  # Adjust batch size if necessary
                        collection.insert_many(batch)
                        batch = []
                except json.JSONDecodeError:
                    print("Warning: Invalid JSON format skipped.")

            if batch:  # Insert any remaining tweets
                collection.insert_many(batch)
    except FileNotFoundError:
        print(f"File {file_name} not found.")
        sys.exit(1)


def main():
    if len(sys.argv) != 3:
        print("Usage: load-json.py <json_file> <mongodb_port>")
        sys.exit(1)

    json_file = sys.argv[1]
    mongodb_port = sys.argv[2]

    client = connect_to_mongodb(mongodb_port)
    collection = create_database_and_collection(client)
    load_json_data(json_file, collection)
    print("Data loading complete.")


if __name__ == "__main__":
    main()
