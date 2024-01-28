from datetime import datetime
from utils import clear_console, press_any_key


def compose_tweet(db, tweet_content):
    try:
        # Prepare the tweet document with all fields, setting non-applicable ones to null
        tweet = {
            "content": tweet_content,
            "renderedContent": tweet_content,  # Assuming rendered content is the same as content
            "date": datetime.now().isoformat(),  # Format date as ISO 8601 string
            "id": None,  # Assuming an ID format, set to null
            "user": {
                "username": "291user",  # Predefined username
                # Setting all other user fields to null
                "displayname": "291user",
                "id": {"$numberLong": None},
                "description": None,
                "rawDescription": None,
                "descriptionUrls": None,
                "verified": None,
                "created": None,
                "followersCount": None,
                "friendsCount": None,
                "statusesCount": None,
                "favouritesCount": None,
                "listedCount": None,
                "mediaCount": None,
                "location": None,
                "protected": None,
                "linkUrl": None,
                "linkTcourl": None,
                "profileImageUrl": None,
                "profileBannerUrl": None,
                "url": None
            },
            "replyCount": None,
            "retweetCount": None,
            "likeCount": None,
            "quoteCount": None,
            "conversationId": {"$numberLong": None},
            "lang": None,
            "source": None,
            "sourceUrl": None,
            "sourceLabel": None,
            "url": None,
            "outlinks": None,
            "tcooutlinks": None,
            "media": None,
            "retweetedTweet": None,
            "quotedTweet": None,
            "mentionedUsers": None
        }

        # Insert the tweet into the database
        collection = db['tweets']  # Assuming 'tweets' is the collection name
        result = collection.insert_one(tweet)

        clear_console()
        # Output result
        if result.inserted_id:
            print("Tweet successfully composed and inserted into the database.")
        else:
            print("Failed to insert the tweet.")

        press_any_key()

    except Exception as e:
        clear_console()
        print(f"An error occurred while composing the tweet: {e}")
        press_any_key()
