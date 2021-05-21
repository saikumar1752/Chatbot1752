import random
import json
import pprint
import nlpcloud
from pymongo import MongoClient
from flask import Flask, jsonify, request

app=Flask(__name__)
nlpapis=[
	"2df4083aa8e71c45a1913a6abee1b5e443dbfdbc",
	"66f926e21f3160c7c917d9d4ef312947250284b6",
	"8833df5d4ff304cf054bbb88b0f767e3ca79c8ba"
]
length=len(nlpapis)
nlpclients=[]
for x in nlpapis:
	nlpclients.append(nlpcloud.Client("roberta-base-squad2", x))
client = MongoClient("mongodb+srv://abhisekkumar:passcode23@internproject-zscmu.mongodb.net/Airbus?retryWrites=true&w=majority")

db=client.ChatbotMessages.Messages
count=0
@app.route("/", methods=["GET", "POST"])
def hello_world():	
	global count
	store=nlpclients[count]
	count=(count+1)%length
	lol=request.data.decode('UTF-8')
	obj=json.loads(lol)
	question=obj['message']
	subjects=db.find()
	answers=[]
	for x in subjects:
		if "content" in x:
			nplmessage=store.question(x["content"], question)
			answers.append([nplmessage["answer"], nplmessage["score"]])
	answers.sort(reverse=True, key=lambda x :x[1])
	print(answers[0][1])
	if answers[0][1]<0.5:
		answer=db.find({"dummy":"true"})
		store=[]
		for x in answer:
			store.append(x["message"])
		store=store[0]
		return jsonify(fulfillmentText=store)
	return jsonify(fulfillmentText=answers[0][0])

if __name__=='__main__':
	app.run(debug=True)
	

