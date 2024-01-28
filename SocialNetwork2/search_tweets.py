from utils import clear_console, press_any_key

def search_tweets(db, keywords):
    try:
        collection = db['tweets']
        # Updated regex pattern to include word boundaries
        regex_pattern = "(?=.*\\b" + "\\b)(?=.*\\b".join(keywords) + "\\b)"
        query = {"content": {"$regex": regex_pattern, "$options": 'i'}}

        # Retrieve all fields from each matching document
        results = collection.find(query)

        return list(results)
    except Exception as e:
        clear_console()
        print(f"An error occurred: {e}")
        press_any_key()
        return []
