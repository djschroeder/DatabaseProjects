import db_connect
import search_tweets
import search_users
import search_top_tweets
import search_top_users
import select_and_display_tweets
import select_and_display_users
import compose_tweet
from utils import *


def main():
    clear_console()
    db = None
    while db is None:
        port = input("Enter MongoDB port: ")
        db = db_connect.connect_to_mongodb(port)

    options = ["Search Tweets",
               "Search Users",
               "Search Top Tweets",
               "Search Top Users",
               "Compose Tweet",
               "Exit"]

    while True:
        clear_console()

        choice = draw_options(options)
        choice = validate_user_input(choice, options)

        if not choice:
            continue

        clear_console()

        if options[choice - 1] == "Search Tweets":
            keywords = input("Enter search keywords, separated by space: ")
            if not validate_empty_input(keywords):
                continue
            results = search_tweets.search_tweets(db, keywords.split())
            select_and_display_tweets.select_and_display_tweets(results)

        elif options[choice - 1] == "Search Users":
            keyword = input("Enter keyword to search for users: ")
            if not validate_empty_input(keyword):
                continue
            results = search_users.search_users(db, keyword)
            select_and_display_users.select_and_display_users(results)

        elif options[choice - 1] == "Search Top Tweets":
            clear_console()

            sort_options = ["Retweet Count",
                            "Like Count",
                            "Quote Count",
                            "Go back"]

            print("Sort by: ")

            field = draw_options(sort_options)
            field = validate_user_input(field, sort_options)

            if not field:
                continue

            if sort_options[field - 1] == "Retweet Count":
                field = 'retweetCount'
            elif sort_options[field - 1] == "Like Count":
                field = 'likeCount'
            elif sort_options[field - 1] == "Quote Count":
                field = 'quoteCount'
            elif sort_options[field - 1] == "Go back":
                continue

            clear_console()

            print("Sorting by: ", field)
            n = input("\nEnter number of tweets to display: ")

            if not validate_empty_input(n):
                continue

            n = validate_is_digit(n)

            if not n:
                continue

            results = search_top_tweets.search_top_tweets(db, field, n)
            select_and_display_tweets.select_and_display_tweets(results)

        elif options[choice - 1] == "Search Top Users":
            clear_console()

            n = input("Enter number of top users to display: ")

            if not validate_empty_input(n):
                continue

            n = validate_is_digit(n)

            if not n:
                continue

            results = search_top_users.search_top_users(db, n)
            select_and_display_users.select_and_display_users(results)

            continue

        elif options[choice - 1] == "Compose Tweet":
            clear_console()
            print("Compose Tweet\n")
            tweet_content = input("Enter tweet content: ")

            if not validate_empty_input(tweet_content):
                continue

            compose_tweet.compose_tweet(db, tweet_content)
            
            continue

        elif options[choice - 1] == "Exit":
            print("Exiting...")
            press_any_key()
            clear_console()
            break


if __name__ == "__main__":
    main()
