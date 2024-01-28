from follows import *

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
