from flask import Flask, jsonify, request, redirect
from flask_pymongo import pymongo

# CONNECTION_STRING = "mongodb+srv://bill:platypus@platypus.kjtat.mongodb.net/LINE_LABEL?retryWrites=true&w=majority"
CONNECTION_STRING = "mongodb+srv://angela:angyeah6@cluster0.gxqmm.mongodb.net/LINE_LABEL?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('LINE_LABEL')
user = pymongo.collection.Collection(db, 'User')
question = pymongo.collection.Collection(db, 'Question')
task = pymongo.collection.Collection(db, 'Task')
