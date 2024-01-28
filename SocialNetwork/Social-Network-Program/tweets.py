import sqlite3
from datetime import datetime

# Fetch tweets and retweets of all followed users
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

# Function counts tweets of user
def countTweets(cursor, user_id):
    cursor.execute(''' SELECT COUNT(*)
                FROM tweets t
                WHERE t.writer = ? ''', 
                (user_id,))
    tweet_count = cursor.fetchone()
    return tweet_count 

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

def searchTweets(cursor):

    user_input = input("Tweet Search: ")
    input_list = user_input.split(" ")
    mentions = []
    tweets = []

    
    for txt in input_list:
        
        txt = txt.lower()
        
        if len(txt) == 0:
            print("Invalid input\n")
            return tweets

        if (txt[0] == "#"):
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