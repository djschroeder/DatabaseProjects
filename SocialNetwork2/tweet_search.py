from utils import clear_console, press_any_key


def search_tweets(db, keywords):
    try:
        collection = db['tweets']
        regex_pattern = "(?=.*" + ")(?=.*".join(keywords) + ")"
        query = {"content": {"$regex": regex_pattern, "$options": 'i'}}

        # Counting the number of documents matching the query
        count = collection.count_documents(query)
        print(f"Number of results: {count}")

        results = collection.find(query, {'_id': 0, 'id': 1, 'date': 1, 'content': 1, 'user.username': 1})
        return list(results)
    except Exception as e:
        clear_console()
        print(f"An error occurred: {e}")
        press_any_key()
        return []
