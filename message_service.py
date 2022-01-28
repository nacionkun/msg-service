#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# import the MongoClient class
from xmlrpc.client import boolean
from pymongo import MongoClient, errors
from bson.json_util import dumps
import json

from flask import Flask, request, jsonify
app = Flask(__name__)


# global variables for MongoDB host (default port is 27017)
DOMAIN = '172.20.0.2'
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

 
@app.route('/messages/delete/single', methods=['POST'])
def delete_single():
    request_json = request.get_json()
    
    if request_json == None:
        return jsonify({'error':"No valid JSON body sent."})

    print(request_json)

    collection.delete_one({"message" : request_json['message']})

    return "Message deleted."


@app.route('/messages/delete/multiple', methods=['POST'])
def delete_multiple():
    request_json = request.get_json()
    
    if request_json == None:
        return jsonify({'error':"No valid JSON body sent."})

    print(request_json)

    collection.delete_many({"recipient" : request_json['recipient']})

    return "Messages deleted."


@app.route('/messages/send', methods=['POST'])
def store_message():
    request_json = request.get_json()
    
    if request_json == None:
        return jsonify({'error':"No valid JSON body sent."})

    message_record = {
        "message" : request_json['message'],
        "recipient" : request_json['recipient'],
        "new_state" : True
    }
    collection.insert_one(message_record)
    return "Message sent."
    
    
@app.route('/messages')
def fetch_all():
    print("Listing all messages:")

    ret_cur = collection.find({})

    list_cur = list(ret_cur)

    json_data = dumps(list_cur, indent = 2)
 
    return json_data


@app.route('/messages/new')
def fetch_new():
    print("Listing new messages:")

    ret_cur = collection.find({"new_state" : True})

    list_cur = list(ret_cur)

    json_data = dumps(list_cur, indent = 2)

    # TODO: Mark as OLD the newly fetched messages

    return json_data


if __name__ == "__main__":
    main()
