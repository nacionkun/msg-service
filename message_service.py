#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# import the MongoClient class
from xmlrpc.client import boolean
from pymongo import MongoClient, errors
import os

from flask import Flask, request, jsonify
app = Flask(__name__)


# global variables for MongoDB host (default port is 27017)
DOMAIN = '172.18.0.2'
PORT = 27017

client = MongoClient(
            host = [ str(DOMAIN) + ":" + str(PORT) ],
            serverSelectionTimeoutMS = 3000, # 3 second timeout
            username = "root",
            password = "1234",
        )

print ("server version:", client.server_info()["version"])
database_names = client.list_database_names()

db = client.messages
collection = db.collection


@app.route('/')
def root():
    return 'MESSAGE SERVICE'


def mark_old(message, recipient):
    present_record = collection.find_one({"message" : message}, 
                                         {"recipient" : recipient})
    new_record = {'$set':{"new_state" : False}}                                   
    collection.update_one(present_record, new_record)
    

def mark_new(message, recipient):
    present_record = collection.find_one({"message" : message}, 
                                         {"recipient" : recipient})
    new_record = {'$set':{"new_state" : True}}                                   
    collection.update_one(present_record, new_record)


def delete_single(message):
    collection.delete_one({"message" : message})


def delete_multiple(recipient):
    collection.delete_many({"recipient" : recipient})
    

@app.route('/messages/send', methods=['POST'])
def store_message():
    request_json = request.get_json()
    print(request_json)
    
    # if request_json == None:
    #     return jsonify({'error':"No valid JSON body sent."})

    print("Sending message..")
    # message_record = {
    #     "message" : message,
    #     "recipient" : recipient,
    #     "new_state" : True
    # }
    # collection.insert_one(message_record)


@app.route('/messages')
def fetch_all():
    print("Listing all messages:")
    result = collection.find({})
    messages_list = list()

    for document in result:
        print(document)
        messages_list = list.append(document)

    return jsonify(messages_list)


@app.route('/messages/new')
def fetch_new():
    print("Listing new messages:")
    result = collection.find({"new_state" : True})
    for document in result:
        print(document)
    return result


if __name__ == "__main__":
    main()
