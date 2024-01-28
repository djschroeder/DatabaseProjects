import sqlite3
from getpass import getpass


# For converting timezone text to float
def to_float(s):
    try:
        return float(s)
    except ValueError:
        return None


# Registers a new user in the system
def register(conn, cursor):
    # Gather user details
    name = input("Name: ")
    email = input("Email: ")
    city = input("City: ")
    timezone = to_float(input("Timezone: "))
    password = input("Password: ")

    if timezone == None: # If timezone failed to be converted to a float
        print("Invalid timezone format")
        return -1
    
    # Generate a new unique user ID
    # Fetches the highest user ID in the system and increments by 1
    cursor.execute("SELECT MAX(usr) FROM users;")
    usr_ID = cursor.fetchone()[0]
    usr_ID = usr_ID + 1 if usr_ID else 1 # Defaults to 1 if the db is empty
    
    try:
        # Insert the new user details into the 'users' table
        cursor.execute(
            '''
            INSERT INTO users (usr, name, email, city, timezone, pwd)
            VALUES (:usr, :name, :email, :city, :timezone, :pwd);
            ''',
            {'usr': usr_ID,
            'name': name, 
            'email': email, 
            'city': city, 
            'timezone': timezone, 
            'pwd': password}
        )
        conn.commit()
    except sqlite3.Error as e:
        print(e)
        return -1
    
    # Informs the user what there unique generated ID is
    print("Your new user ID is:", usr_ID)
    return usr_ID


# Validates(aka login) a user
def validateUser(cursor, user_id):
    password = getpass("Password: ") # getpass() masks the password input
    cursor.execute(  # Queries the users stored password
        ''' 
        SELECT *
        FROM users
        WHERE usr=?;
        ''',
        (user_id, )
    )
    result = cursor.fetchone()
    if result != None:
        return password == result[1] 
    return False