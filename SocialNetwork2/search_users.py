from utils import clear_console, press_any_key

def search_users(db, keywords):
    try:
        # Split the keywords string and focus only on the first keyword
        first_keyword = keywords.split()[0] if keywords else ''

        # Updated regex pattern for partial matching with word boundaries
        regex_pattern = f"\\b{first_keyword}\\b"
        query = {"$or": [{"user.displayname": {"$regex": regex_pattern, "$options": 'i'}},
                         {"user.location": {"$regex": regex_pattern, "$options": 'i'}}]}

        # Retrieve matching documents
        results = db['tweets'].find(query, {"user": 1, "_id": 0})

        users = list(results)

        # Creating a dictionary to store unique users by their username
        unique_users = {}
        for user in users:
            user_data = user['user']
            username = user_data.get('username')
            if username not in unique_users:
                unique_users[username] = user_data

        # Return the list of unique users
        return list(unique_users.values())

    except Exception as e:
        clear_console()
        print(f"An error occurred: {e}")
        press_any_key()
        return []
