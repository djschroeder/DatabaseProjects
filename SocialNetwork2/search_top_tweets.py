from utils import clear_console, press_any_key


def search_top_tweets(db, field, n):
    try:
        collection = db['tweets']
        query = {}  # Empty query to match all tweets
        sort_field = [(field, -1)]  # Sort in descending order
        results = collection.find(query).sort(sort_field).limit(n)
        return list(results)
    except Exception as e:
        clear_console()
        print(f"An error occurred: {e}")
        press_any_key()
        return []
