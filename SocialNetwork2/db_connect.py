import pymongo
import pymongo.errors as pymongo_errors
from utils import clear_console, press_any_key


def connect_to_mongodb(port):
    """ Connect to the MongoDB server on the given port and verify the connection. """
    clear_console()
    try:
        # Attempt to create a connection to the MongoDB instance
        client = pymongo.MongoClient('localhost', int(port), serverSelectionTimeoutMS=5000)

        # Try to fetch the server info (a quick way to check if the server is operational)
        client.server_info()

        return client['291db']

    except pymongo_errors.ServerSelectionTimeoutError:
        print(f"Failed to connect to MongoDB on port {port}. Timeout occurred.")
    except pymongo_errors.ConnectionFailure as e:
        print(f"Could not connect to MongoDB: {e}")
    except Exception as e:
        print(f"An error occurred while connecting to MongoDB: {e}")

    print("\nAre you sure MongoDB is running on the specified port?")
    press_any_key()

    return None
