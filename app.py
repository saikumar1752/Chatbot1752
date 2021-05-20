import random
import json
import pprint
from pymongo import MongoClient
from flask import Flask, jsonify, request
app=Flask(__name__)

client = MongoClient("mongodb+srv://abhisekkumar:passcode23@internproject-zscmu.mongodb.net/Airbus?retryWrites=true&w=majority")
db=client.ChatbotMessages.Messages
@app.route("/", methods=["GET", "POST"])
def hello_world():
	lol=request.data.decode('UTF-8')
	obj=json.loads(lol)
	question=obj['message']
	print(question)
	answer=db.find({"question":question})
	res=""
	for x in answer:
		print(x['answer'])
		res=x['answer']
	if res!="":
		return jsonify(fulfillmentText=res)

	no_response=db.find({"question":"no_response"})
	store=[]
	res=""
	for x in no_response:
		store.append(x)
		res=x['answer']
	return jsonify(fulfillmentText=res)

if __name__=='__main__':
	app.run(debug=True)

