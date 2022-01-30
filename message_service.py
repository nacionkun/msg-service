#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from pymongo import MongoClient, errors
from bson.json_util import dumps

from flask import Flask, request, jsonify
app = Flask(__name__)


# Global variables for MongoDB host (default port is 27017)
# DOMAIN = '172.19.0.2'
DOMAIN = 'localhost'
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
    return 'MESSAGE SERVICE\n'


def mark_old(message, recipient):
    present_record = collection.find_one({"message": message}, 
                                         {"recipient": recipient})
    new_record = {'$set':{"new_state": False}}                                   
    collection.update_one(present_record, new_record)
    

def mark_new(message, recipient):
    present_record = collection.find_one({"message": message}, 
                                         {"recipient": recipient})
    new_record = {'$set':{"new_state": True}}                                   
    collection.update_one(present_record, new_record)

 
@app.route('/messages/delete/single', methods=['POST'])
def delete_single():
    request_json = request.get_json()
    
    if request_json == None:
        return jsonify({'Error':"No valid JSON body sent."})

    message_str = request_json['message']

    if not message_str:
        return "Please enter message to delete.\n"

    collection.delete_one({"message": request_json['message']})

    return "(Single) message delete function executed.\n"


@app.route('/messages/delete/multiple', methods=['POST'])
def delete_multiple():
    request_json = request.get_json()
    
    if request_json == None:
        return jsonify({'Error':"No valid JSON body sent."})

    recipient_str = request_json['recipient']

    if not recipient_str:
        return "Please specify recipient to delete multiple messages.\n"

    collection.delete_many({"recipient": request_json['recipient']})

    return "(Multiple) messages delete function executed.\n"


@app.route('/messages/send', methods=['POST'])
def store_message():
    request_json = request.get_json()
    
    if request_json == None:
        return jsonify({'Error':"No valid JSON body sent."})

    recipient_str = request_json['recipient']
    message_str = request_json['message']

    if not recipient_str:
        return "Please specify recipient!\n"
        
    if not message_str:
        return "Empty message. Please enter valid message!\n"

    message_record = {
        "message": request_json['message'],
        "recipient": request_json['recipient'],
        "new_state": True
    }

    collection.insert_one(message_record)

    return "Message sent.\n"
    
    
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

    ret_cur = collection.find({ "new_state": True })

    list_cur = list(ret_cur)
    # TODO: Fetch messages ordered by time (or ObjectId index)
    json_data = dumps(list_cur, indent = 2)

    result = collection.update_many( 
                {
                    "new_state": True
                },
                {
                    "$set": { "new_state" : False }
                }
    )
    print ("Messages updated: ", result.matched_count)

    return json_data


if __name__ == "__main__":
    main()
