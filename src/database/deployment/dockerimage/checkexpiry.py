#! /usr/local/bin/python3
import sys
import datetime
import psycopg2
import os
from dotenv import load_dotenv
import logging
from sql_funcs import getAllLates, markLost

# Configure logging to write to logfile
logging.basicConfig(filename='lost.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
load_dotenv()
# Access environment variables
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE = os.getenv('DATABASE')
MINS= os.getenv('DURATION')

#table indizies
ID = 0
LENGTH = 1
HIGHT = 2
LASTGATE = 3
LASTSEENAT = 4
EXPECTEDNEXT = 5
STATUS = 6

mins = 120 #int(MINS)
def main():
    try:
        #Establish a connection to PostgerSQL database
        connection = psycopg2.connect(dbname=DATABASE, user=DATABASE_USER, password=DATABASE_PASSWORD, host=DATABASE_HOST, port=DATABASE_PORT)
        
        # Create a cursor object using the connection
        cursor = connection.cursor()

        # Display PostgreSQL server version
        cursor.execute('SELECT version();')
        db_version = cursor.fetchone()
        print(f"Connected to PostgreSQL (version: {db_version[0]})")
    except psycopg2.Error as error:
        print("Error while connecting to PostgreSQL:", error)

    stopTime = datetime.datetime.now() + datetime.timedelta(minutes=mins)
    print("stopping evaluation at " + str(stopTime))

    while datetime.datetime.now() < stopTime:
        ret = getAllLates(cursor)
        for val in ret:
            id = val[ID]
            status = val[STATUS]
            #lost bit is not yet set, apply changes
            if (status & 0b1000) == 0:
                #set lost bit and mark entry as lost
                status = status | 0b1000
                markLost(connection, cursor, id, status)
                # Define a formatted string message
                message = "Parcel missing with ID: {Id}. Parcel last seen at Gate {gate} at {time}. Expected next Gate was {nextgate} at {nexttime}".format(Id=id, gate=val[LASTGATE], time=val[LASTSEENAT], nextgate=(val[LASTGATE] + 1), nexttime=val[EXPECTEDNEXT])
                # Log the formatted message at the INFO level
                logging.warning(message)
                print("lost parcel detected")
    print("evaluation stopped")
    try:
        # Close communication with the database
        cursor.close()
        connection.close()
        print("connection to database closed")
    except psycopg2.Error as error:
        print("Error while connecting to PostgreSQL:", error)

#Call main
if __name__ == "__main__":
   # if len(sys.argv) != 2:
   #     print("faslche anzahl an commandozeilenargumenten - minuten werden auf 5 gesetzt")
   #     mins = 1
   # else:
   #     mins = int(sys.argv[1])
    main()
