def search_users(db, keyword):
    # Assuming the collection is named 'tweets'
    collection = db['tweets']
    query = {
        "$or": [
            {"user.displayname": {"$regex": keyword, "$options": 'i'}},
            {"user.location": {"$regex": keyword, "$options": 'i'}}
        ]
    }
    projection = {
        '_id': 0,
        'user.username': 1,
        'user.displayname': 1,
        'user.location': 1
    }

    results = collection.find(query, projection).distinct("user")
    return list(results)
