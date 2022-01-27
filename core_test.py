#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# import the MongoClient class
from xmlrpc.client import boolean
from pymongo import MongoClient, errors

# global variables for MongoDB host (default port is 27017)
DOMAIN = '172.18.0.2'
PORT = 27017


def fetch_new(collection):
    print("new messages:")
    result = collection.find({"new_state" : True})
    for document in result:
        print(document)
    return result


def fetch_all(collection):
    print("all messages:")
    result = collection.find({})
    for document in result:
        print(document)
    return result


def mark_old(collection, message, recipient):
    present_record = collection.find_one({"message" : message}, 
                                         {"recipient" : recipient})
    new_record = {'$set':{"new_state" : False}}                                   
    collection.update_one(present_record, new_record)
    

def mark_new(collection, message, recipient):
    present_record = collection.find_one({"message" : message}, 
                                         {"recipient" : recipient})
    new_record = {'$set':{"new_state" : True}}                                   
    collection.update_one(present_record, new_record)


def delete_single(collection, message):
    collection.delete_one({"message" : message})


def delete_multiple(collection, recipient):
    collection.delete_many({"recipient" : recipient})
    

def store(collection, recipient, message):
    message_record = {
        "message" : message,
        "recipient" : recipient,
        "new_state" : True
    }
    collection.insert_one(message_record)


def create_collection(client):
    db = client.messages
    collection = db.collection
    return collection


def connect():
    try:
        client = MongoClient(
            host = [ str(DOMAIN) + ":" + str(PORT) ],
            serverSelectionTimeoutMS = 3000, # 3 second timeout
            username = "root",
            password = "1234",
        )

        print ("server version:", client.server_info()["version"])
        database_names = client.list_database_names()

    except errors.ServerSelectionTimeoutError as err:
        # set the client and DB name list to 'None' and `[]` if exception
        client = None
        database_names = []

        # catch pymongo.errors.ServerSelectionTimeoutError
        print ("pymongo ERROR:", err)

    print ("\ndatabases:", database_names)
    return client


def main():

    client = connect()
    collection = create_collection(client)

    # cleanup before test
    # collection.drop()
    
    # test fetch empty
    fetch_new(collection)

    # test store messages
    # store(collection, "kk@gmail.com", "Ground control to major tom.")
    # store(collection, "kk@gmail.com", "Houston we have a problem.")
    # store(collection, "Kosmo Kramer", "Giddyup!")
    # store(collection, "Kosmo Kramer", "Oolala!")
    # store(collection, "Kosmo Kramer", "Newman!")
    # store(collection, "1234567890", "I know what you did last summer.")
    # fetch_new(collection)

    # test delete single message
    # delete_single(collection, "I know what you did last summer.")
    # fetch_new(collection)

    # mark message as old and check fetch new if updated
    # mark_old(collection, "Oolala!", "Kosmo Kramer")
    fetch_new(collection)
    fetch_all(collection)

    # test delete multiple messages and fetch collection
    # delete_multiple(collection, "kk@gmail.com")
    # delete_multiple(collection, "Kosmo Kramer")
    # fetch_all(collection)
    

if __name__ == "__main__":
    main()
