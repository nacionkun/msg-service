#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from pymongo import MongoClient, errors

mongo_client = None

# Global variables for MongoDB host (default port is 27017)
# DOMAIN = '172.19.0.2'
DOMAIN = 'localhost'
PORT = 27017


class mongoData:

    def __init__(self, app):
        self.app = app

    def __get_mongo_client(self):
        global mongo_client

        if not mongo_client:
            mongo_client = MongoClient(
                host = [ str(DOMAIN) + ":" + str(PORT) ],
                serverSelectionTimeoutMS = 3000, # 3 second timeout
                username = "root",
                password = "1234",
            )

        return mongo_client

    def get_mongo_client_server_version(self):
        return self.__get_mongo_client().server_info()["version"]
    
    def get_database_names(self):
        return self.__get_mongo_client().list_database_names()

    def get_db(self):
        return self.__get_mongo_client().messages
    
    def get_collection(self):
        return self.__get_mongo_client().db.collection
        
