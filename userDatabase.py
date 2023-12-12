import sqlite3

class DatabaseSignIn():
    def __init__(self, userInfoDict):  # userInfoDict -> name, surname, birth day, password
        self.userInfoDict = userInfoDict
        dataBase = sqlite3.connect('users.db')
        cursor = dataBase.cursor()

        # Create the 'workerUsers' table if it doesn't exist
        query1 = '''CREATE TABLE IF NOT EXISTS workerUsers(
                    userId INTEGER PRIMARY KEY AUTOINCREMENT,
                    userFirstName TEXT NOT NULL,
                    userSurname TEXT NOT NULL,
                    userBirthDate TEXT NOT NULL,
                    userName TEXT NOT NULL,
                    userPassword TEXT NOT NULL)'''
        cursor.execute(query1)
        dataBase.commit()

        # Insert user information into the 'workerUsers' table
        query2 = 'INSERT INTO workerUsers(userFirstName, userSurname, userBirthDate, userName, userPassword) VALUES(?, ?, ?, ?, ?)'
        userInfo = (self.userInfoDict['name'], self.userInfoDict['surname'], self.userInfoDict['birthdate'], self.userInfoDict['username'], self.userInfoDict['password'])
        cursor.execute(query2, userInfo)
        dataBase.commit()

        # Close the database connection
        dataBase.close()

def DatabaseLogIn(userName, userPassword):
    dataBase = sqlite3.connect('users.db')
    cursor = dataBase.cursor()

    # Check if the provided username and password match an entry in the 'workerUsers' table
    cursor.execute('SELECT userId FROM workerUsers WHERE userName = ? AND userPassword = ?', (userName, userPassword))
    userId = cursor.fetchall()

    # Close the database connection
    dataBase.close()

    # Return True if a matching entry is found, False otherwise
    return len(userId) > 0
