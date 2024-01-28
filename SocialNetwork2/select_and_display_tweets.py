import display_tweet_details
import display_tweets
from utils import clear_console, press_any_key


def select_and_display_tweets(tweets):
    clear_console()
    if not tweets:
        print("No results found.")
        press_any_key()
        return

    while True:
        clear_console()
        display_tweets.display_tweets(tweets)

        try:
            selection = input(
                "Enter the number of the tweet to view details, or type 'back' to return: ").strip().lower()

            if selection == 'back':
                break

            selection = int(selection) - 1
            if 0 <= selection < len(tweets):
                clear_console()
                display_tweet_details.display_tweet_details(tweets[selection])
                input("\nPress Enter to return to the list...")
            else:
                clear_console()
                print("Invalid selection. Please enter a number from the list or type 'back' to return.")
                press_any_key()
        except ValueError:
            clear_console()
            print("Invalid input. Please enter a numerical value or type 'back'.")
            press_any_key()
