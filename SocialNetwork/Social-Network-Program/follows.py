import sqlite3
from datetime import datetime

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