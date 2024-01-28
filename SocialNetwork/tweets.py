import sqlite3
from datetime import datetime


def userSearch(cursor, key_word):
    cursor.execute('''
    SELECT u.usr, u.name, u.city
    FROM users u
    WHERE LOWER(u.name) LIKE LOWER(?)
    OR LOWER(u.city) LIKE LOWER(?)
    ORDER BY LENGTH(u.name), LENGTH(u.city)''', ('%' + key_word + '%')) 
    search_result = cursor.fetchall()
    return search_result


def composeTweet(conn, cursor, user_id, replyto = None):
    # Get input from user
    tweet_text = input("Enter your tweet: ")

    # Extract hashtags by filtering words starting with '#'
    words = tweet_text.split()
    hashtags = [word[1:] for word in words if word.startswith('#')]

    # Get next Tweet ID
    cursor.execute("SELECT MAX(tid) FROM tweets;")
    max_tid = cursor.fetchone()[0]
    tweet_id = (max_tid + 1) if max_tid else 1

    # Current date and time
    current_date = datetime.now().strftime("%Y-%m-%d")

    try:
        # Insert the tweet into database
        cursor.execute("""
            INSERT INTO tweets (tid, writer, tdate, text, replyto)
            VALUES (?, ?, ?, ?, ?);
        """, (tweet_id, user_id, current_date, tweet_text, replyto))
        conn.commit()
        print("Your Tweet is posted successfully!")
        print()
        # Insert hashtags into database
        if hashtags:
            for hashtag in hashtags:
                # Ensure the hashtag exists in the hashtags table
                cursor.execute("INSERT OR IGNORE INTO hashtags (term) VALUES (?);", (hashtag,))
                conn.commit()
                
                # Then, insert the mention of the hashtag for this tweet
                cursor.execute("""
                    INSERT INTO mentions (tid, term)
                    VALUES (?, ?);
                """, (tweet_id, hashtag))
                conn.commit()
    except sqlite3.Error as error:
        print("Error:", error)

# Function to fetch tweets and retweets from the database for the given user on initial login
def getTweets(cursor, user_ID):
    # Execute SQL query to select tweets and retweets of the people the user follows
    cursor.execute(
        '''
        SELECT t.tid, u.name, t.text, t.tdate
        FROM follows f
        JOIN users u ON u.usr = f.flwee
        JOIN tweets t ON f.flwee = t.writer
        WHERE f.flwer = ?

        UNION

        SELECT t.tid, u.name, t.text, r.rdate as tdate
        FROM follows f
        JOIN users u ON u.usr = f.flwee
        JOIN retweets r ON f.flwee = r.usr
        JOIN tweets t ON t.tid = r.tid
        WHERE f.flwer = ?

        ORDER BY tdate DESC;
        ''',
        (user_ID, user_ID)
    )
    # Fetch all results from the executed query
    tweetList = cursor.fetchall()
    return tweetList


def searchTweets(cursor):

    user_input = input("Tweet Search: ")
    input_list = user_input.split(" ")
    mentions = []
    tweets = []
    for txt in input_list:
        txt = txt.lower()

        if txt[0] == "#":
            txt = txt[1:]
            # Search in mentions table
            cursor.execute('SELECT tid FROM mentions m WHERE LOWER(m.term)=?;', (txt,))
            result = cursor.fetchall()
            mentions += [num[0] for num in result]  # Converts tid tuple to int
            
        else:
            # Search in tweets table
            cursor.execute('SELECT tid FROM tweets t WHERE LOWER(t.text) LIKE ?;', ('%' + txt + '%',))
            result = cursor.fetchall()
            tweets += [num[0] for num in result]    # Converts tid tuple to int
            
    tid_list = list(set(mentions + tweets))  
    tid_str = ", ".join("?" * len(tid_list))

    query = f"SELECT t.tid, u.name, t.text, t.tdate FROM tweets t JOIN users u ON t.writer = u.usr WHERE t.tid IN ({tid_str}) ORDER BY t.tdate DESC"
    cursor.execute(query, tid_list)
    tweets = cursor.fetchall()
    return tweets 
    
# Function to retweet a tweet
def retweet(conn, cursor, user_ID, tweet_ID):
    # Get the current date in yyyy-mm-dd format
    current_date = datetime.now()
    formatted_date = current_date.strftime('%Y-%m-%d')
    # Execute SQL command to insert a new row into the retweets table
    cursor.execute(
        '''
        INSERT INTO retweets (usr, tid, rdate)
        VALUES (?, ?, ?)
        ''',
        (user_ID, tweet_ID, formatted_date)
    )
    # Commit the transaction to the database
    conn.commit()
    # Inform the user that the retweet was successful
    print("Retweet successful")
    print()

# Function to display statistics of a tweet
def stats(cursor, tweet_ID):
    # Initialize counters for replies and retweets
    reply_count = 0
    retweet_count = 0
    # Execute SQL query to count the number of replies to the tweet
    cursor.execute(
        '''
        SELECT COUNT(*)
        FROM tweets
        WHERE replyto = ?
        ''',
        (tweet_ID, )
    )
    # Fetch the reply count from the query result
    reply_count = cursor.fetchone()
    # Execute SQL query to count the number of retweets of the tweetS
    cursor.execute(
        '''
        SELECT COUNT(*)
        FROM retweets
        WHERE tid = ?
        ''',
        (tweet_ID, )
    )
    # Fetch the retweet count from the query result
    retweet_count = cursor.fetchone()
        # Print the statistics
    print("# of replies: " + str(reply_count[0]) + ", # of retweets: " + str(retweet_count[0]))
    print()

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
            print("Invalid input")

# Function counts tweets of user
def countTweets(cursor, user_id):
    cursor.execute(''' SELECT COUNT(*)
                FROM tweets t
                WHERE t.writer = ? ''', 
                (user_id,))
    tweet_count = cursor.fetchone()
    return tweet_count

# Function to count number of followers of user
def countFollowers(cursor, user_id):
    cursor.execute('''  SELECT COUNT(f.flwee)
                        FROM follows f
                        WHERE f.flwee = ?
                   ''',
                   (user_id,))
    count = cursor.fetchone()
    return count[0]

# Funtion to count number of users current user follows
def followingCount(cursor, user_id):
    cursor.execute('''  SELECT COUNT(f.flwer)
                        FROM follows f
                        WHERE f.flwer = ?
                   ''',
                   (user_id,))   
    count = cursor.fetchone()
    return count[0]

# Function to get list of all followers of a user
def getFollowers(cursor, usr):
    cursor.execute('''  SELECT u.usr, u.name
                        FROM follows f, users u
                        WHERE f.flwee = ?
                        AND u.usr = f.flwer''', (usr,))
    followers = cursor.fetchall()
    return followers

# Function to get all tweets of a selected user
def getUserTweets(cursor, user_id):
    cursor.execute('''  SELECT t.tid, u.name, t.text, t.tdate
                        FROM users u
                        JOIN tweets t ON u.usr = t.writer
                        WHERE u.usr = ?
                   
                        UNION

                        SELECT t.tid, u.name, t.text, t.tdate
                        FROM users u
                        JOIN retweets r ON u.usr = r.usr
                        JOIN tweets t ON t.tid = r.tid
                        WHERE u.usr = ?

                        ORDER BY t.tdate DESC;
                   ''', (user_id, user_id))
    tweet_list = cursor.fetchall()
    return tweet_list

# Function to follow a user
def followUser(conn, cursor, target_user, current_user):
    current_date = datetime.now()
    formatted_date = current_date.strftime('%Y-%m-%d')
    try:
        cursor.execute('''  INSERT INTO follows (flwer, flwee, start_date)
                            VALUES (?,?,?)
                       ''', (current_user, target_user, formatted_date))
        conn.commit()
        return 1
    except sqlite3.Error as e:
        print("You already follow this user!")
        print()
        return -1

# Function to print follower stats of a selected user
def printFollowers(conn, cursor, follower_list, current_user_id):
    if (len(follower_list) == 0):
        print("Oops! User does not follow anyone!")
        return
    
    # Prints follower list and displays new menu options
    for follower in range(0, len(follower_list)):
        print(str(follower + 1) + ": ", follower_list[follower][1])
    print("\n[1 - ", len(follower_list),"]: Stats of selected user, b: back")
    
    # Input validation
    while True:
        action = input(">>> ")
        print()
        if action.lower() == "b":
            return
        try:
            action = int(action)
            if 1 <= action <= len(follower_list):
                printFollowStats(conn, cursor, follower_list[action - 1], current_user_id)
                break
            else:
                print("Invalid input")
        except ValueError:
            print("Invalid input")

# Function to print follower stats, follow selected user
def printFollowStats(conn, cursor, follower, current_user_id):
    
    # All values needed for output
    user_id = follower[0]
    user_name = follower[1]
    follower_count = countFollowers(cursor, user_id)
    following_count = followingCount(cursor, user_id)
    tweetList = getUserTweets(cursor, user_id)
    tweet_count = len(tweetList)

    showOptions = True
    printIndex = 0
    tweetMax = 3

    print("\nName: ", user_name)
    print("Tweet Count: ", tweet_count, "  Follower Count: ", follower_count, "  Following Count: ", following_count)
    print()
    
    while(1):
        # Print navigation and selection options
        if showOptions: # Don't print if previous input was invalid
            if tweet_count:
                printTweets(tweetList, printIndex, tweetMax)
                print("N: next, P: previous, F: follow user, B: back")
            else:
                print("User has no tweets")
                print("F: follow user, B: back")
        # Inner loop for handling user input and navigation
        showOptions = True
        action = input(">>> ").lower()
        print()

        if action == 'n': # Show page for next group of 3 tweets
            if printIndex + tweetMax < len(tweetList):
                printIndex += tweetMax

        elif action == 'p': # Show page for previous group of 3 tweets
            if printIndex - tweetMax >= 0:
                printIndex -= tweetMax

        elif action == 'f': # Follow current user
            if (followUser(conn, cursor, user_id, current_user_id) == 1):
                print("You now follow ", user_name, "!")
                print()
            return
        
        elif action == 'b': # back
            return
        
        else:
            showOptions = False
            print("Invalid input")
            
    return

# Function to handle user search
def userSearch(conn, cursor, current_user_id):
    
    # Input validation
    valid = False
    while (not valid):
        try:
            print("Please enter a single keyword to search.")
            keyword = input(">>> ").lower()
            if (len(keyword.split()) != 1):
                raise Exception
            else:
                valid = True
        except:
            print("Error! Only ONE word can be entered.")
      
    # Setup for search menu      
    printIndex = 0
    userMax = 5
    showOptions = True             
    users = getUsers(cursor, keyword)
    
    while(1):
        if showOptions:
            if len(users) != 0:
                printTweets(users, printIndex, userMax)   
                print("N: next, P: previous, [index]: select user, B: back")
            else:
                print()
                print("No users found")
                print("B: back")
            # Inner loop for handling user input and navigation
        showOptions = True
        action = input(">>> ").lower()
        print()

        if action == 'n': # Show page for next group of 5 users
            if printIndex + userMax < len(users):
                printIndex += userMax

        elif action == 'p': # Show page for previous group of 5 users
            if printIndex - userMax >= 0:
                printIndex -= userMax
                
        elif action == 'b': # Back
            return 
          
        else: # Select user index
            try:
                userIndex = int(action) - 1
                printFollowStats(conn, cursor, users[userIndex], current_user_id)
                
            except: # if program falls through to here, input was invalid
                showOptions = False
                print("Invalid input")
    return

# Function to query for name or city with keyword
def getUsers(cursor, keyword):
    cursor.execute('''
    SELECT u.usr, u.name, u.city
    FROM users u
    WHERE LOWER(u.name) LIKE LOWER(?)
    OR LOWER(u.city) LIKE LOWER(?)
    ORDER BY LENGTH(u.name), LENGTH(u.city)''', ('%' + keyword + '%', '%' + keyword + '%')) 
    search_result = cursor.fetchall()
    users = []

    for user in search_result:
        usr = user + ('',)
        users.append(usr)

    # Now extended_search_result contains the modified tuples
    return users   

# Function prints tweets, but also users and city
def printTweets(tweetList, printIndex, tweetMax):
    # Print tweets in pages of size tweetMax
    for tweet in range(printIndex, printIndex + tweetMax):
        if (tweet < len(tweetList)):
            name = tweetList[tweet][1]
            text = tweetList[tweet][2]
            date = tweetList[tweet][3]
            print(str(tweet + 1) + ")", name + ':', text, "| " + date)
    print()


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
            compose_tweet(conn, cursor, user_ID)

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
    
