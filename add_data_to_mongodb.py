import os
from flask import Flask, jsonify, request, redirect
from flask_pymongo import pymongo

CONNECTION_STRING = os.getenv('CONNECTION_STRING', None)
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('LINE_LABEL')
db.User.drop()
db.Level.drop()
db.Task.drop()
db.Transaction.drop()
db.Label.drop()
db.Question.drop()

