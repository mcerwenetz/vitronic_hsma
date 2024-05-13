#! /usr/local/bin/python3

import psycopg2
import os
from dotenv import load_dotenv
from sql_funcs import clearTable, addEntry, getEntries, updateTable, printEntry

# Load environment variables from .env file
load_dotenv()
# Access environment variables
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE = os.getenv('DATABASE')

def test(connection,cursor):
    try:
        # Define the INSERT statement with placeholders (%s)
        query = "SELECT lastgate FROM paket WHERE id=(%s);"

        # Sample data to be inserted
        user_data = (5,)
        # Execute the INSERT statement
        cursor.execute(query, user_data)
        # Commit the transaction
        connection.commit()
        ret = cursor.fetchone()
        print(ret[0])
    except psycopg2.Error as error:
        # Handle any error that may occur during the INSERT operation
        print("Error inserting data:", error)
    return

def default():
    """if the specified argument is not known, this method will be called"""
    print("command not known")
    return

def getInput():
    """read new command from stdin"""
    print("Kommando eingeben:")
    return input()

def get(cursor):
    ret = getEntries(cursor)
    for entry in ret:
        printEntry(entry)
        print("\n----------\n")
    return

def main():
    try:
        # Establish a connection to the PostgreSQL database
        connection = psycopg2.connect(dbname=DATABASE, user=DATABASE_USER, password=DATABASE_PASSWORD, host=DATABASE_HOST, port=DATABASE_PORT)

        # Create a cursor object using the connection
        cursor = connection.cursor()

        # Display PostgreSQL server version
        cursor.execute('SELECT version();')
        db_version = cursor.fetchone()
        print(f"Connected to PostgreSQL (version: {db_version[0]})")

    except psycopg2.Error as error:
        print("Error while connecting to PostgreSQL:", error)

    data = ""
    data = getInput()
    while data != "q":
        if data == "add":
            addEntry(connection, cursor)
            print("entry added to db")
        elif data == "get":
            get(cursor)
        elif data == "clear":
            clearTable(connection, cursor)
            print("database table cleared")
        elif "update" in data:
            cmd , id = data.split(' ')
            updateTable(connection, cursor, id)
            print("Paket with ID "+ str(id) + " updated")
        elif data == "test":
            test(connection, cursor)
        else:
            default()
        data = getInput()

    try:
        # Close communication with the database
        cursor.close()
        connection.close()
        print("connection to database closed")
        
    except psycopg2.Error as error:
        print("Error while closing the DB Connection:", error)

    print("done")


#Call main
if __name__ == "__main__":
    main()