import textwrap


def display_tweets(tweets):

    for i, tweet in enumerate(tweets, start=1):
        content_preview = textwrap.shorten(tweet.get('content', ''), width=80, placeholder="...")
        print(f"{i}. Tweet ID: {tweet.get('id', 'N/A')}")
        print(f"   Date: {tweet.get('date', 'N/A')}")
        print(f"   User: @{tweet.get('user', {}).get('username', 'N/A')}")
        print(f"   Content: {content_preview}\n")
        print("-" * 100)
