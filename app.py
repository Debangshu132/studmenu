#Python libraries that we need to import for our bot
import random
from pymongo import MongoClient
from flask import Flask, request,render_template
from pymessenger.bot import Bot
import os
import requests

import json
from decisionTree import decision,listOfExams,askQuestion,handleResults,decisionRightWrong
from intelligence import BRAIN
import time
app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
bot = Bot (ACCESS_TOKEN)
#ps=PorterStemmer()
RID=''
#We will receive messages that Facebook sends our bot at this endpoint
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    global RID
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook."""
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
      # get whatever message a user sent the bot
      output = request.get_json()
      #for first time only check if this is the get started click or no
      checkReferral(output)
      checkPostback(output)  
      for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                RID=recipient_id 
                if message['message'].get('text'):
                    typingon=pay({"recipient":{"id":recipient_id},"sender_action":"typing_on"})
                    if  message['message'].get('quick_reply'):  
                      secretcode= message['message']['quick_reply']['payload']
                      if secretcode=='hint':
                            hint=getUserInformation(recipient_id,'lasthint')
                            sendLastOptionsQuickReply(recipient_id,hint)
                            return "Message Processed"
                      if secretcode=='right':
                          
                        currtopic=getUserInformation(recipient_id,"currenttopic")
                        #currtotal=str(currtopic)+'total'
                        #currright=str(currtopic)+'right'
                        updateUsersInformation(recipient_id,insidequestion=False,totalquestionasked=int(getUserInformation(recipient_id,'totalquestionasked'))+1)
                        updateUsersInformation(recipient_id,totalquestionright=int(getUserInformation(recipient_id,'totalquestionright'))+1)
                        updateUsersInformation(recipient_id,**{str(currtopic)+'total':int(getUserInformation(recipient_id,str(str(currtopic)+'total')))+1})
                        updateUsersInformation(recipient_id,**{str(currtopic)+'right':int(getUserInformation(recipient_id,str(str(currtopic)+'right')))+1})
                        noofconsecutiveright=getUserInformation(recipient_id,'noofconsecutiveright')
                        updateUsersInformation(recipient_id,noofconsecutivewrong=0)
                        updateUsersInformation(recipient_id,noofconsecutiveright=noofconsecutiveright+1)
                        reply=decisionRightWrong('right', noofconsecutiveright)
                        #send_message(recipient_id, "dummy","dummy",reply)
                        if getUserInformation(recipient_id,'currenttopic')=='aptitude':
                            quickreply(recipient_id,['Another One','Go Back','Results','I am Bored!'], reply)
                        else:
                            quickreply(recipient_id,['Another One','Go Back','Results','I am Bored!'], reply+'\n'+getUserInformation(recipient_id,'lastsolution'))
                        
                        return "Message Processed"
                      if secretcode=='wrong':
                        
                        updateUsersInformation(recipient_id,insidequestion=False,totalquestionasked=int(getUserInformation(recipient_id,'totalquestionasked'))+1)
                        rightAns=getUserInformation(recipient_id,'lastRightAnswer')
                        
                        noofconsecutivewrong=getUserInformation(recipient_id,'noofconsecutivewrong')
                        updateUsersInformation(recipient_id,noofconsecutiveright=0)
                        updateUsersInformation(recipient_id,noofconsecutivewrong=noofconsecutivewrong+1)
                        
                        
                        
                        currtopic=getUserInformation(recipient_id,"currenttopic")
                        #currtotal=str(currtopic)+'total'
                        updateUsersInformation(recipient_id,**{str(currtopic)+'total':int(getUserInformation(recipient_id,str(str(currtopic)+'total')))+1})
                        
                        
                        reply=decisionRightWrong('wrong', noofconsecutivewrong)
                        #send_message(recipient_id, "dummy","dummy",reply+ ' ,the right answer is: '+'\n'+rightAns)
                        quickreply(recipient_id,['Try Another','Go Back','Results','I am Bored!'],reply+ ' ,the right answer is: '+'\n'+rightAns+'\n'+getUserInformation(recipient_id,'lastsolution'))
                        
                        return "Message Processed"
                    
                    topic,mood,response = get_message(recipient_id,message['message'].get('text'))
                    #checkPostback(output)
                    isQuickReply=checkQuickReply(message['message'].get('text'),recipient_id)
                    
                    isQuickReplyHint=checkQuickReply(response,recipient_id)
                    isCalculator=checkCalculator(recipient_id,message['message'].get('text'))
                    if isQuickReply==False and isQuickReplyHint==False and isCalculator==False :
                        quickreply(recipient_id,['Lets test', 'I am Bored!'],response)
                        #sendLastOptionsQuickReply(recipient_id,'kya be')
                        return "Message Processed"
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    response = ['(y)',':)',":D"]
                    
                    quickreply(recipient_id,['Lets test', 'I am Bored!'],random.choice(response))
               
    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#chooses a random message to send to the user
def get_message(recipient_id,query):
      
  try:  
    punctuation=[',','.','!','?']
    for i in punctuation:
        query=query.replace(i,"")
    topic,mood,response=BRAIN(query)
    return(topic,mood,response)
  except:
    return 'dummy','dummy','I am sorry I didnot quite get what you are saying'    
def quickreply(id,listofitems,text):
    payload = {"recipient": {"id": id}, "message": {"text":text,"quick_replies": []}}
    for item in listofitems:
        payload['message']['quick_replies'].append({"content_type":"text","title":str(item),"payload":str(item)})   
    pay(payload)
    return 'success'
  
def pay(payload):
  request_endpoint = "https://graph.facebook.com/v2.6/me/messages?access_token="+os.environ['ACCESS_TOKEN']
  #payload={"recipient":{"id":recipient_id},"sender_action":"typing_on"}
  response=requests.post(
    request_endpoint, params=bot.auth_args,
            json=payload )
  result = response.json()
  return result
def checkReferral(output):
     if output['entry'][0]['messaging'][0].get('referral'):
      id=  output['entry'][0]['messaging'][0]['sender']['id']  
      a=requests.get("https://graph.facebook.com/"+id+"?fields=first_name,last_name,profile_pic&access_token="+ACCESS_TOKEN)
      data=a.json()
      name=data['first_name']
      fulladdress=str(output['entry'][0]['messaging'][0]['referral']['ref'])
      fulladdress=fulladdress.split("_")
       
      restaurant=fulladdress[0]
      try:   
           tableno=fulladdress[1]
      except:
            tableno="none"    
      handleUser(id,fulladdress,name,restaurant,tableno)
    
def checkPostback(output):
 if output['entry'][0]['messaging'][0].get('postback'):
    id=  output['entry'][0]['messaging'][0]['sender']['id']  
    a=requests.get("https://graph.facebook.com/"+id+"?fields=first_name,last_name,profile_pic&access_token="+ACCESS_TOKEN)
    data=a.json()
    name=data['first_name']
    if output['entry'][0]['messaging'][0]['postback']['payload']=='StartMan':
       if output['entry'][0]['messaging'][0]['postback'].get('referral'):
         fulladdress=str(output['entry'][0]['messaging'][0]['postback']['referral']['ref'])
         fulladdress=fulladdress.split("_")
         restaurant=fulladdress[0]
         try:   
           tableno=fulladdress[1]
         except:
            tableno="none"    
         
         handleUser(id,fulladdress,name,restaurant,tableno)
       else:
        welcome="Welcome! "+name+" please open the camera and long press to scan the QR code!"
       
       
    if output['entry'][0]['messaging'][0]['postback']['payload']=='waiter':
        quickreply(id,['Napkins','Spoons',"Water","Talk to waiter"],"Calling waiter what do you want?")
        
def handleUser(id,fulladdress,name,restaurant,tableno):
    userCondition=checkUserCondition(id)
    if userCondition=="none":
        createUser(id,fulladdress,name,restaurant,tableno)
        return True
    if userCondition=="waiter":    
        executeWaiterCode(id,fulladdress,name,restaurant,tableno)
        return True
    if userCondition=="consumer":
        if tableno=="none":
            createUser(id,fulladdress,name,restaurant,tableno)
            return True
        else:    
         executeConsumerCode(id,fulladdress,name,restaurant,tableno)
         return True
    else:
        return False
def checkUserCondition(id):
    MONGODB_URI = "mongodb://Debangshu:Starrynight.1@ds163694.mlab.com:63694/brilu"
    client = MongoClient(MONGODB_URI, connectTimeoutMS=30000)
    db = client.get_database("brilu")
    col = db["users"]
    cursor = col.find()
    waiterFind = cursor[0]
    consumerFind=cursor[1]
    if waiterFind.get(id):
        return "waiter"
    if consumerFind.get(id):
        return "consumer"
    else:
        return "none"
def createUser(id,fulladdress,name,restaurant,tableno):
    if len(fulladdress)==1:
       
        executeWaiterCode(id,fulladdress,name,restaurant,tableno)
        updateWaitersInformation(id,name=name)
    else:
           
        executeConsumerCode(id,fulladdress,name,restaurant,tableno)
        updateConsumersInformation(id,name=name)
def executeConsumerCode(id,fulladdress,name,restaurant,tableno):
       welcome='Welcome!'+name+" you are sitting in restaurant "+restaurant+" in table number "+ tableno+" I am your host today :)"
       send_message(id,'a','a', welcome)
       instruction="To open menu press Open Menu, To call the waiter press Call Waiter"
       button= [{ "type": "web_url","url": "studmenu.herokuapp.com/menu", "title": "Menu" },
               {"type":"postback","title":"Waiter","payload":"waiter"}] 
       bot.send_button_message(id,'To open menu press Open Menu ',button) 
       updateConsumersInformation(id,name=name,currentRestaurant=restaurant,currentTable=tableno)  
def executeWaiterCode(id,fulladdress,name,restaurant,tableno):
    if tableno=="none":
      send_message(id,"a","a","welcome "+name+" from now you are a waiter in "+restaurant+ " restaurant")
      updateWaitersInformation(id,name=name,currentRestaurant=restaurant) 
      updateRestaurantsWaitersInformation(restaurant, **{id:name})  
    else:    
      table=getRestaurantsTableInformation(restaurant,tableno) 
      if table['waiter']=="":
            send_message(id,"a","a","You will be serving this table from now on!Table no. :"+tableno)
      else:
        send_message(id,"a","a","waiting for the previous waiter's approval")
        #send_message(table['waiter'],"a","a",name+" Wants to serve your table number "+ tableno)
        prompt=name+" Wants to serve your table number "+ tableno
        quickreply(table['waiter'],['Accept','Deny'],prompt)    
      #updateWaitersInformation(id,currentTable=tableno)
    
    
def checkQuickReply(text,id): 
         try: 
           msges,listofitems=decision(text)
           if text=="Call Waiter":
             quickreply(id,["napkins","spoon","water","Talk to waiter","Open Menu"],"calling waiter what do you want") 
             return True
           if text=="Open Menu": 
                 button= [{ "type": "web_url","url": "https://www.google.com/", "title": "Open Menu" }]
                 bot.send_button_message(id,'To open menu press Open Menu ',button)
                 return True
         except:
            return False    

       
        
#uses PyMessenger to send response to user
def send_message(recipient_id, topic,mood,response):
    #sends user the text message provided via input response parameter
    if mood=='call':
          bot.send_button_message(recipient_id,'Not Satisfied with my responses? Call Our Representative! ',response)
          return 'success'  
    bot.send_text_message(recipient_id, response)
    return "success"

def updateWaitersInformation(ID, **kwargs):
    MONGODB_URI = "mongodb://Debangshu:Starrynight.1@ds163694.mlab.com:63694/brilu"
    client = MongoClient(MONGODB_URI, connectTimeoutMS=30000)
    db = client.get_database("brilu")
    for key in kwargs:
        db.users.update({"_id" : "waiter"}, {"$set":{str(ID)+"."+str(key): kwargs[key]}},upsert=True);
    return(0)
def updateConsumersInformation(ID, **kwargs):
    MONGODB_URI = "mongodb://Debangshu:Starrynight.1@ds163694.mlab.com:63694/brilu"
    client = MongoClient(MONGODB_URI, connectTimeoutMS=30000)
    db = client.get_database("brilu")
    for key in kwargs:
        db.users.update({"_id" : "consumer"}, {"$set":{str(ID)+"."+str(key): kwargs[key]}},upsert=True);
    return(0)
def updateRestaurantsWaitersInformation(nameOfRestaurant, **kwargs):
    MONGODB_URI = "mongodb://Debangshu:Starrynight.1@ds163694.mlab.com:63694/brilu"
    client = MongoClient(MONGODB_URI, connectTimeoutMS=30000)
    db = client.get_database("brilu")
    waiters=getRestaurantsInformation(nameOfRestaurant,"waiters")
    for key in kwargs:
        waiters[key]=str(kwargs[key])
    print(waiters)
    db.restaurants.update({"_id" : "restaurant"}, {"$set":{str(nameOfRestaurant)+".waiters": waiters}},upsert=True);
    return(0)
def getRestaurantsInformation(nameOfRestaurant,property):
    MONGODB_URI = "mongodb://Debangshu:Starrynight.1@ds163694.mlab.com:63694/brilu"
    client = MongoClient(MONGODB_URI, connectTimeoutMS=30000)
    db = client.get_database("brilu")
    col = db["restaurants"]
    cursor = col.find()
    restaurant = cursor[0]
    return(restaurant[nameOfRestaurant][property])
def getRestaurantsTableInformation(nameOfRestaurant,tableno):
    MONGODB_URI = "mongodb://Debangshu:Starrynight.1@ds163694.mlab.com:63694/brilu"
    client = MongoClient(MONGODB_URI, connectTimeoutMS=30000)
    db = client.get_database("brilu")
    col = db["restaurants"]
    cursor = col.find()
    restaurant = cursor[0]
    return(restaurant[nameOfRestaurant]["tables"][str(tableno)])

def getUserInformation(id,property):
    MONGODB_URI = "mongodb://Debangshu:Starrynight.1@ds163694.mlab.com:63694/brilu"
    client = MongoClient(MONGODB_URI, connectTimeoutMS=30000)
    db = client.get_database("brilu")
    col = db["users"]
    cursor = col.find()
    userInfo = cursor[0]
    return(userInfo[id][property])



     
    



@app.route("/menu", methods=['GET', 'POST'])
def menu():
         return "hey man"
         #return render_template('chart.html')
    
def initializeUser(id,category):
    a=requests.get("https://graph.facebook.com/"+id+"?fields=first_name,last_name,profile_pic&access_token="+ACCESS_TOKEN)
    data=a.json()
    name=data['first_name']
    if category=="waiter":
        updateWaitersInformation(id,name=name,name1="")
    if category=="consumer":
        updateConsumersInformation(id,name=name,name1="")    
    

if __name__ == "__main__":
    app.run()
