from printing import printTweets, printFollowStats

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