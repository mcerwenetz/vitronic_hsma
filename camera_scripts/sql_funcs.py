import PIL.Image
import psycopg2
import random
import datetime
import numpy as np
import cv2
import PIL
from io import BytesIO
#status of different packages
# STATI[0] - OK | STATI[1] - DEFECTIVE | STATI[3] - CHINA | STATI[4] - LOST
STATI = [1,2,4,8]

#table indizies
ID = 0
LENGTH = 1
HIGHT = 2
LASTGATE = 3
LASTSEENAT = 4
EXPECTEDNEXT = 5
STATUS = 6
FEATUREVEC = 7

#time to next gate
SECONDS = 30

def clearTable(connection, cursor):
    """this method will delete all entries from the database table"""
    try:
        # Define the delete statement to delete all entries
        delete_query = "DELETE FROM paket;"
        # Execute the INSERT statement
        cursor.execute(delete_query)
    except psycopg2.Error as error:
        # Handle any error that may occur during the INSERT operation
        print("Error clearing data:", error)

    return

def insertNewParcel(connection, cursor, gate, classification, features:np.ndarray, lenght, height):
    """this method will add a new parcel to the parceldump table"""
    lenghtDB = lenght
    heightDB = height
    lastgateDB = gate
    lastSeenDB = datetime.datetime.now()
    expectedNextGateDB = datetime.datetime.now() + datetime.timedelta(seconds=SECONDS)
    statusDB = classification # 1: ok | 2: defekt
    featureVecDB = features.tobytes()
    try:
        # Define the INSERT statement with placeholders (%s)
        insert_query = "INSERT INTO parceldump(lenght , height , lastgate , lastseenat , expectednext , status, features) VALUES (%s, %s, %s, %s, %s, %s, %s);"

        # Sample data to be inserted
        user_data = (lenghtDB , heightDB, lastgateDB , lastSeenDB, expectedNextGateDB, statusDB, psycopg2.Binary(featureVecDB))

        # Execute the INSERT statement
        cursor.execute(insert_query, user_data)

        # Commit the transaction
        connection.commit()

    except psycopg2.Error as error:
        # Handle any error that may occur during the INSERT operation
        print("Error inserting data:", error)
    return

def updateParcel(connection, cursor, parcelId ,gate, classification, features:np.ndarray, lenght, height):
    """this method will update an exisitng parcel entry in the parceldump db"""
    lenghtDB = lenght
    heightDB = height
    lastgateDB = gate
    lastSeenDB = datetime.datetime.now()
    expectedNextGateDB = datetime.datetime.now() + datetime.timedelta(seconds=SECONDS)
    statusDB = classification # 1: ok | 2: defekt

    featureVecDB = features.tobytes()
    try:
        # Define the INSERT statement with placeholders (%s)
        update_query = "INSERT INTO parceldump(lenght , height , lastgate , lastseenat , expectednext , status, features) VALUES (%s, %s, %s, %s, %s, %s, %s);"
        update_query = "UPDATE parceldump SET lenght=(%s), height=(%s), lastgate=(%s),lastseenat=(%s), expectednext=(%s), status=(%s) WHERE id = (%s);"
        # Sample data to be inserted
        user_data = (lenghtDB , heightDB, lastgateDB , lastSeenDB, expectedNextGateDB, statusDB, parcelId) #change feature vec to new feautreVEc or keep old feature vec?

        # Execute the INSERT statement
        cursor.execute(update_query, user_data)

        # Commit the transaction
        connection.commit()

    except psycopg2.Error as error:
        # Handle any error that may occur during the INSERT operation
        print("Error inserting data:", error)
    return


def addEntry(connection, cursor, gate, classification, features:np.ndarray, length = 1, height = 1): # classification: 1 good 2 bad
    """this method will find an existing db entry according to the feature vec. If no matching vector is found, a new entry is added"""
    #get all feature vectors and id -> feat vec vergleichen -> wenns übereinstimmt updaten! sont neuer Eintrag
    bf = cv2.BFMatcher()
    try:
        #get all ids and  featureVecs
        query = "SELECT id, features FROM parceldump;"
        cursor.execute(query)
        erg = cursor.fetchall()
        parcelIdFound = -1 #id of the parcel with the matching feature vec     
        
        if len(erg) == 0:
            insertNewParcel(connection, cursor, gate, classification, features, length, height)
            return

        
        dic = dict()
        for val in erg:
            bf = cv2.BFMatcher()
            id = val[0]
            feature = np.frombuffer(val[1],dtype=np.uint8)
            feature.reshape(500,32)

            print(type(features[0][0][0]))
            print(type(feature[0][0]))

            matches = bf.knnMatch(features, feature, k=2) #features is the new classified image feature vector and feature is the feature vec of an old db entry
            dic[id] = 0
            for m , n in matches:
                if m.distance < 0.98 * n.distance:
                    dic[id] = dic[id] + 1
        maxValue = max(dic.values())
        maxKey=-1
        maxKey = [i for i in dic.keys() if dic[i] == maxValue ]
        print("Max key: " + str(maxKey))     
        
        if maxValue  < 80:  #if parcelId is -1, then no parcel was found that matches an exisitng feature vector
            insertNewParcel(connection, cursor, gate, classification, features, length, height)
        else: # update the parcel entry with the found parcelId
            updateParcel(connection, cursor, maxKey, gate, classification, features, length, height)

    except psycopg2.Error as error:
        # Handle any error that may occur during the INSERT operation
        print("Error inserting data:", error)
    return

def addEntryOld(connection, cursor, gate, classification, features:np.ndarray, length = 1, height = 1): # classification: 1 good 2 bad
    """this method will add a new parcel to the parceldump table"""
    lenghtDB = length
    heightDB = height
    lastgateDB = gate
    lastSeenDB = datetime.datetime.now()
    expectedNextGateDB = datetime.datetime.now() + datetime.timedelta(seconds=SECONDS)
    statusDB = classification # 1: ok | 2: defekt
    featureVecDB = features.tolist()

    #get all feature vectors and id -> feat vec vergleichen -> wenns übereinstimmt updaten! sont neuer Eintrag

    try:
        # Define the INSERT statement with placeholders (%s)
        insert_query = "INSERT INTO parceldump(lenght , height , lastgate , lastseenat , expectednext , status, features) VALUES (%s, %s, %s, %s, %s, %s, %s);"

        # Sample data to be inserted
        user_data = (lenghtDB , heightDB, lastgateDB , lastSeenDB, expectedNextGateDB, statusDB, featureVecDB)

        # Execute the INSERT statement
        cursor.execute(insert_query, user_data)

        # Commit the transaction
        connection.commit()

    except psycopg2.Error as error:
        # Handle any error that may occur during the INSERT operation
        print("Error inserting data:", error)
    return

def printEntry(entry):
    """this method prints an entry of the db table formatted to the stdout"""
    entries=["ID", "length", "height", "lastgate", "lastseenat", "expectedNext", "status", "featureVec"]
    for i, val in enumerate(entry):
        if(entries[i] != "status"):
            print((entries[i]).ljust(13) + ": " + str(val))
        else:
            binrepresentation= (bin(val)[2:]).zfill(4)
            print((entries[i]).ljust(13) + ": " + str(binrepresentation))
    print("\n"+ ('#') * 41+"\n")
    return

def updateTable(connection, cursor, paketId):
    try:
        # Define the UPDATE statement with placeholders (%s)
        getpaket_query = "SELECT * FROM paket WHERE id = (%s)"
        # Sample data to be inserted
        paket = (paketId,)
        # Execute the UPDATE statement
        cursor.execute(getpaket_query, paket)
        ret = cursor.fetchone()
        if ret == None:
            print("No package found with id: " + str(paketId))
            return

        gate = ret[LASTGATE] + 1
        #unset the lost status bit if it was set before
        status = ((ret[STATUS]) & 0b0111)
        # gate = (cursor.fetchone())[0] + 1
        lastSeen = datetime.datetime.now()
        expectedNextGate = datetime.datetime.now() + datetime.timedelta(seconds=SECONDS)
        user_data = (gate, lastSeen, expectedNextGate, status, paketId)
        
        #create update query
        update_query = "UPDATE paket SET lastgate=(%s), lastseenat=(%s), expectedNext=(%s), status=(%s) WHERE id = (%s);"
        # Execute the UPDATE statement
        cursor.execute(update_query, user_data)
        # Commit the transaction
        connection.commit()

    except psycopg2.Error as error:
        # Handle any error that may occur during the UPDATE operation
        print("Error updating data:", error)
    return

def getEntries(curs):
    """this method will get all entries from the database"""
    try:
        get_query = "SELECT * FROM paket;"
        curs.execute(get_query)
        return curs.fetchall()
    except psycopg2.Error as error:
        # Handle any error that may occur during the GET operation
        print("Error retreiving data:", error)

def getAllLates(cursor):
    """this method will return a list of all database enries, where the expectedNext datetime has already passed"""
    try:
        now = datetime.datetime.now()
        get_query = "SELECT * FROM paket WHERE expectednext < (%s);"
        timestamp = (now,)
        # Execute the GET statement
        cursor.execute(get_query, timestamp)
        return cursor.fetchall()
    except psycopg2.Error as error:
        # Handle any error that may occur during the GET operation
        print("Error inserting data:", error)

def markLost(connection, cursor, paketId, paketstatus):
    """this method will set the status given with @paketstatus to the database entry. 
        It is used to mark a db entry as lost"""
    try:
        user_data = (paketstatus, paketId)
        #create update query
        update_query = "UPDATE paket SET status=(%s) WHERE id = (%s);"
        # Execute the UPDATE statement
        cursor.execute(update_query, user_data)
        # Commit the transaction
        connection.commit()

    except psycopg2.Error as error:
        # Handle any error that may occur during the Update operation
        print("Error inserting data:", error)
    return 
