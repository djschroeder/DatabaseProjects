import sqlite3
import sys
import os

from tweets import *
from follows import *
from user_info import *
from authentication import *
from printing import printFollowers

# Connect to SQLite database
def connect(file_path):
    global connection, cursor
    if not os.path.exists(file_path): 
        # Only opens existing db. Will not create a new empty db.
        print("Database does not exist.")
        exit(1)
    conn = sqlite3.connect(file_path)
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys=ON;') 
    conn.commit()
    return conn, cursor

# Function to select a tweet and perform actions such as stats, reply, retweet, or go back
def tweetOptions(conn, cursor, user_ID, tweet_ID): 
    invalid = True
    print("S: stats, R: reply, T: retweet, B: back")
    while(invalid):
        action = input(">>>").lower()
        print()
        if action == 's':
            invalid = False
            stats(cursor, tweet_ID)
        elif action == 'r':
            invalid = False
            composeTweet(conn, cursor, user_ID, tweet_ID)
        elif action == 't':
            invalid = False
            retweet(conn, cursor, user_ID, tweet_ID)
        elif action == 'b':
            return
        else:
            print("Invalid input 1")


def homepage(conn, cursor, user_ID): # Main function to display the homepage and handle user input.
    print()
    print("UserID: " + user_ID)

    printIndex = 0 # For tracking which 5 tweets to show
    tweetMax = 5 #
    showOptions = True # Use to not repeatedly print options when an invalid input was entered
    tweetList = getTweets(cursor, user_ID) # Fetch tweets for initial login display
    
    while(1):
        # Print navigation and selection options
        if showOptions: # Dont print if previous input was invalid
            printTweets(tweetList, printIndex, tweetMax)
            print("P: previous, N: next, [id]: select tweet id, T: search tweets, S: Show followed users tweets")
            print("C: compose tweet, U: search users, F: list followers, L: logout, E: exit")

        # Inner loop for handling user input and navigation
        showOptions = True
        action = input(">>>").lower()
        print()

        if action == 'n': # Show page for next group of 5 tweets
            if printIndex + 5 < len(tweetList):
                printIndex += 5

        elif action == 'p': # Show page for previous group of 5 tweets
            if printIndex - 5 >= 0:
                printIndex -= 5

        elif action == 'c': # Compose a tweet
            composeTweet(conn, cursor, user_ID)

        elif action == 't': # Search tweets
            tweetList = searchTweets(cursor)
        
        elif action == 's':
            tweetList = getTweets(cursor, user_ID)

        elif action == 'u': # Search Users
            userSearch(conn, cursor, user_ID)

        elif action == 'f': # List followers
            follower_list = getFollowers(cursor, user_ID)
            printFollowers(conn, cursor, follower_list, user_ID)
            
        elif action == 'l': # Logout
            return
        
        elif action == 'e': # Exit program   
            conn.commit()
            conn.close()
            exit(0)

        else: # Select tweet ID
            try:
                tweetIndex = int(action) - 1
                print("Selected tweet: " + action)
                tweet_ID = tweetList[tweetIndex][0]
                tweetOptions(conn, cursor, user_ID, tweet_ID)
            except: # if program falls through to here, input was invalid
                showOptions = False
                print("Invalid input")
    

def loginMenu(conn, cursor):
    invalid = True 
    selection = None

    while True:
        # Print the main menu
        print()
        print("<<< Binary Ballers Social Network >>>")
        print(" 1 - Login")
        print(" 2 - Register")
        print(" 3 - Exit")

        # Loop until the user provides a valid option
        while (invalid):
            # Try except block for int casting input
            try:
                selection = int(input("Select a number: "))
                if selection in (1,2,3):
                    invalid = False
                else:
                    print("Invalid selection.")
                    print()
            except:
                print("Invalid selection.")
                print()

        # Handling for each menu option
        if selection == 1:
            # User login selected
            user_id = input("User ID: ")
            if validateUser(cursor, user_id):
                return user_id
            else:
                invalid = True
                print("Invalid user ID or password")
                print()

        elif selection == 2:
            # Register new user selected
            user_id = register(conn, cursor)
            if  user_id > 0:
                return user_id
            else:
                invalid = True
                print("Error creating new user")
                print()

        else: # Selection == 3
            conn.commit()
            conn.close()
            exit(0) # Exit program


def main ():
    if len(sys.argv) < 2:
        print("Provide database filepath using input redirection")
    else:
        file_path = sys.argv[1]
        conn, cursor = connect(file_path)
        while (1):
            # login loop, if player logs out, loop starts for new user
            # options to terminate program in loginMenu() and homepage()
            user_ID = loginMenu(conn, cursor)
            homepage(conn, cursor, user_ID)


if __name__ == "__main__":
    main()