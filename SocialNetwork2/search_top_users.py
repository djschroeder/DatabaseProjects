from utils import clear_console, press_any_key


def search_top_users(db, n):
    try:
        collection = db['tweets']  # Assuming the user data is within the 'tweets' collection
        # Aggregate to sort and limit the top users based on followersCount
        pipeline = [
            {"$group": {
                "_id": "$user.username",
                "userDetails": {"$first": "$user"}
            }},
            {"$sort": {"userDetails.followersCount": -1}},
            {"$limit": n}
        ]
        results = collection.aggregate(pipeline)

        # Extracting user details from the aggregation results
        top_users = [doc['userDetails'] for doc in results]

        return top_users
    except Exception as e:
        clear_console()
        print(f"An error occurred: {e}")
        press_any_key()
        return []
