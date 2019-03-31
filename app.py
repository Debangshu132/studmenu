#Python libraries that we need to import for our bot
import random
from pymongo import MongoClient
from flask import Flask, request,render_template
from pymessenger.bot import Bot
import os
from flask_socketio import SocketIO,send,emit
import requests
import urllib
from flask_cors import CORS
import json
from decisionTree import decision,listOfExams,askQuestion,handleResults,decisionRightWrong
from intelligence import BRAIN
import time
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
bot = Bot (ACCESS_TOKEN)
consumer_id="initial"
waiter_id=""
@app.route("/menu", methods=['GET', 'POST'])
def menu():
         #menu=getRestaurantsInformation(restaurant,"menu")  
         #return "hello"
         return 'yeay it worked dumbo'

#We will receive messages that Facebook sends our bot at this endpoint
@socketio.on('canirefresh',namespace="/test")
def handle_my_custom_event(msg):
    print("yo refresh the page")     
    emit('okrefreshpage', msg, broadcast=True)
@app.route("/", methods=['GET', 'POST'])
def receive_message():
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
                      if secretcode.find('TableChangeAccept') != -1:
                            secretcode=secretcode.split('|')
                            updateRestaurantsTablesInformation(secretcode[2],secretcode[3], waiter=secretcode[1])
                            send_message(recipient_id,"a","a","Your table number has been changed successfully!")
                            send_message(secretcode[1],"a","a","Congracts your request has been accepted! :)")
                            return "Message Processed"
                      if secretcode.find('TableChangeDeny') != -1:
                            secretcode=secretcode.split('|')
                            send_message(secretcode[1],"a","a","Sorry the waiter has not accepted your table number :(")
                            return "Message Processed"
                    topic,mood,response = get_message(recipient_id,message['message'].get('text'))
                    isQuickReply=checkQuickReply(message['message'].get('text'),recipient_id)
                    
                    #isQuickReplyHint=checkQuickReply(response,recipient_id,name,restaurant,tableno)
                    if isQuickReply==False  :
                        quickreply(recipient_id,['Dummy Menu', 'Dummy Waiter'],"I didnot get what you are saying")
                        return "Message Processed"
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    response = ['(y)',':)',":D"]
                    
                    quickreply(recipient_id,['I am Bored!'],random.choice(response))
               
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
def quickreplyDifferentPayload(id,listofitems,listofpayloads,text):
    payload = {"recipient": {"id": id}, "message": {"text":text,"quick_replies": []}}
    for i in range(0,len(listofitems)):
        payload['message']['quick_replies'].append({"content_type":"text","title":str(listofitems[i]),"payload":str(listofpayloads[i])})   
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
      global consumer_id   
    
      id=  output['entry'][0]['messaging'][0]['sender']['id']  
      consumer_id=id
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
      return name,restaurant,tableno
        
    
def checkPostback(output):

 if output['entry'][0]['messaging'][0].get('postback'):
    global consumer_id     
    id=  output['entry'][0]['messaging'][0]['sender']['id']  
    consumer_id=id
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
         welcome="please choose one from below!"
         quickreply(id,['Gurgaon','Noida','Delhi'],welcome)
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
        updateWaitersInformation(id,name=name,currentRestaurant=restaurant)
        executeWaiterCode(id,fulladdress,name,restaurant,tableno)
        
    else:
        updateConsumersInformation(id,name=name,currentRestaurant=restaurant,currentTable=tableno)   
        executeConsumerCode(id,fulladdress,name,restaurant,tableno)
       
def executeConsumerCode(id,fulladdress,name,restaurant,tableno):
       welcome='Welcome!'+name+" you are sitting in restaurant "+restaurant+" I am your host today :)"
       #send_message(id,'a','a', welcome)
       updateConsumersInformation(id,name=name,currentRestaurant=restaurant,currentTable=tableno)  
       updateRestaurantsTablesConsumerInformation(restaurant,tableno, name)
       restaurant=getConsumerInformation(id,"currentRestaurant")
       tableno=getConsumerInformation(id,"currentTable")
       tables=getRestaurantsInformation(restaurant,"tables")
       table=tables[tableno]
       waiterid=table['waiter']
       waiter=getRestaurantsInformation(restaurant,"waiters")  
       yourwaiter=waiter[waiterid]["name"]  
         
         
       instruction="Our waiter "+ yourwaiter+" will be serving you,To open menu press Open Menu, To call "+yourwaiter+" press Call Waiter"
       button= [{ "type": "web_url","url": "https://studmenuweb.herokuapp.com/menu/"+getConsumerInformation(id,"currentRestaurant"),
                 "title": "Menu","messenger_extensions": True},
               {"type":"postback","title":"Waiter","payload":"waiter"}] 
       bot.send_button_message(id,instruction,button) 
       
       updateConsumersInformation(id,name=name,currentRestaurant=restaurant,currentTable=tableno)  
def executeWaiterCode(id,fulladdress,name,restaurant,tableno):
    if tableno=="none":
      send_message(id,"a","a","welcome "+name+" from now you are a waiter in "+restaurant+ " restaurant")
      updateWaitersInformation(id,name=name,currentRestaurant=restaurant,tableno=tableno) 
      info={"name":name,"picurl":"","active":True,"activetables":[]}   
      updateRestaurantsWaitersInformation(restaurant, **{id:info})  
    else:    
      table=getRestaurantsTableInformation(restaurant,tableno) 
      if table['waiter']=="":
            updateRestaurantsTablesInformation(restaurant,tableno, waiter=id)
            send_message(id,"a","a","You will be serving this table from now on!Table no. :"+tableno)
            
      else:
        send_message(id,"a","a","waiting for the previous waiter's approval")
        #send_message(table['waiter'],"a","a",name+" Wants to serve your table number "+ tableno)
        prompt=name+" Wants to serve your table number "+ tableno
        #quickreply(table['waiter'],['Accept Change','Deny Change'],prompt)  
        quickreplyDifferentPayload(table['waiter'],['Accept','Deny'],['TableChangeAccept | '+str(id)+'|'+str(restaurant)+'|'+str(tableno),'TableChangeDeny |'+str(id)],prompt)
      #updateWaitersInformation(id,currentTable=tableno)
    
    
def checkQuickReply(text,id): 
           restaurant=getConsumerInformation(id,"currentRestaurant")
                 
           tableno=getConsumerInformation(id,"currentTable")
           tables=getRestaurantsInformation(restaurant,"tables")
           tableno="1"
           table=tables["1"]
           waiterid=table['waiter'] 
                         
           if text=="Call Waiter":
             quickreply(id,["napkins","spoon","water","Talk to waiter","Open Menu"],"calling waiter what do you want") 
             return True
           if text=="Napkins":
               send_message(waiterid,"a","a"," table number"+ tableno+"is asking for napkins")
               button= [{ "type": "web_url","url": "https://studmenuweb.herokuapp.com/menu/"+getConsumerInformation(id,"currentRestaurant"),"messenger_extensions": True, "title": "Menu" },
               {"type":"postback","title":"Waiter","payload":"waiter"}] 
               bot.send_button_message(id,'Request sent! Your waiter will be arriving soon! ',button) 
               return True
           if text=="Spoons":
               send_message(waiterid,"a","a"," table number"+ tableno+"is asking for spoons")
               button= [{ "type": "web_url","url":  "https://studmenuweb.herokuapp.com/menu/"+getConsumerInformation(id,"currentRestaurant"),"messenger_extensions":True, "title": "Menu" },
               {"type":"postback","title":"Waiter","payload":"waiter"}] 
               bot.send_button_message(id,'Request sent! Your waiter will be arriving soon! ',button) 
               return True
           if text=="Water":
               send_message(waiterid,"a","a"," table number"+ tableno+"is asking for water")
               button= [{ "type": "web_url","url":  "https://studmenuweb.herokuapp.com/menu/"+getConsumerInformation(id,"currentRestaurant"),"messenger_extensions":True, "title": "Menu" },
               {"type":"postback","title":"Waiter","payload":"waiter"}] 
               bot.send_button_message(id,'Request sent! Your waiter will be arriving soon! ',button) 
               return True 
           if text=="Talk to waiter":
               send_message(waiterid,"a","a"," table number"+ tableno+" wants to talk")
               button= [{ "type": "web_url","url":  "https://studmenuweb.herokuapp.com/menu/"+getConsumerInformation(id,"currentRestaurant"),"messenger_extensions": True, "title": "Menu" },
               {"type":"postback","title":"Waiter","payload":"waiter"}] 
               bot.send_button_message(id,'Request sent! Your waiter will be arriving soon! ',button) 
               return True 
           if text=="Accept Order":
               #send_message(waiterid,"a","a"," table number"+ tableno+"is asking for water")
               button= [{ "type": "web_url","url":  "https://studmenuweb.herokuapp.com/menu/"+getConsumerInformation(id,"currentRestaurant"),"messenger_extensions":True, "title": "Menu" },
               {"type":"postback","title":"Waiter","payload":"waiter"}] 
               bot.send_button_message(id,'Hurray! your ordered has been accepted ',button) 
               return True 
           if text=="Deny Order":
               #send_message(waiterid,"a","a"," table number"+ tableno+"is asking for water")
               button= [{ "type": "web_url","url":  "https://studmenuweb.herokuapp.com/menu/"+getConsumerInformation(id,"currentRestaurant"),"messenger_extensions":True, "title": "Menu" },
               {"type":"postback","title":"Waiter","payload":"waiter"}] 
               bot.send_button_message(id,'Sorry Your order has been denied',button) 
               return True 
          
           else: 
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
    col = db["restaurants"]
    cursor = col.find()
    restaurant = cursor[0]
    db.restaurants.update({"_id" : "restaurant"}, {"$push":{str(currentRestaurant)+".waiters."+str(ID)+".activetables": tableno}},upsert=True);
         
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

def updateRestaurantsCartInformation(nameOfRestaurant,tableno, **kwargs):
    MONGODB_URI = "mongodb://Debangshu:Starrynight.1@ds163694.mlab.com:63694/brilu"
    client = MongoClient(MONGODB_URI, connectTimeoutMS=30000)
    db = client.get_database("brilu")
    tables=getRestaurantsInformation(nameOfRestaurant,"tables")
    table=tables[tableno]
    cart=table["cart"]
    for key in kwargs:
      firstname=kwargs[key]["firstname"]
      db.restaurants.update({"_id" : "restaurant"}, {"$set":{str(nameOfRestaurant)+".tables."+str(tableno)+".cart."+str(key)+".firstname": firstname}},upsert=True);
      cartdata=kwargs[key]["mycart"]
      for individualorder in cartdata:
         db.restaurants.update({"_id" : "restaurant"}, {"$push":{str(nameOfRestaurant)+".tables."+str(tableno)+".cart."+str(key)+".mycart": individualorder}},upsert=True);
    return(0)
def updateRestaurantsStatusInformation(nameOfRestaurant,tableno,id, acceptdeny,allOrBucket):
    MONGODB_URI = "mongodb://Debangshu:Starrynight.1@ds163694.mlab.com:63694/brilu"
    client = MongoClient(MONGODB_URI, connectTimeoutMS=30000)
    db = client.get_database("brilu")
    tables=getRestaurantsInformation(nameOfRestaurant,"tables")
    table=tables[tableno]
    cart=table["cart"]
    cartdata=cart[id]
    mycart=cartdata["mycart"]
    if allOrBucket=="changeall":     
     for atomicorderindex in range(0,len(mycart)):
        db.restaurants.update({"_id" : "restaurant"}, {"$set":{str(nameOfRestaurant)+".tables."+str(tableno)+".cart."+str(id)+".mycart."+str(atomicorderindex)+".status": acceptdeny}},upsert=True);
    db.restaurants.update({"_id" : "restaurant"}, {"$set":{str(nameOfRestaurant)+".tables."+str(tableno)+".cart."+str(id)+".status": acceptdeny}},upsert=True);
    
    return(0)
         
def helpRestaurantCheckout(nameOfRestaurant,tableno):
    MONGODB_URI = "mongodb://Debangshu:Starrynight.1@ds163694.mlab.com:63694/brilu"
    client = MongoClient(MONGODB_URI, connectTimeoutMS=30000)
    db = client.get_database("brilu")
    tables=getRestaurantsInformation(nameOfRestaurant,"tables")
    table=tables[tableno]
    cart=table["cart"]
    for consumerid in cart.keys():
         updateConsumersInformation(consumerid,currentRestaurant='none',currentTable='none')
    updateRestaurantsTablesInformation(nameOfRestaurant,tableno, cart={})     
    updateRestaurantsTablesInformation(nameOfRestaurant,tableno, consumer=[])
    return(0)    
def updateRestaurantsTablesConsumerInformation(nameOfRestaurant,tableno, consumer_id):
    MONGODB_URI = "mongodb://Debangshu:Starrynight.1@ds163694.mlab.com:63694/brilu"
    client = MongoClient(MONGODB_URI, connectTimeoutMS=30000)
    db = client.get_database("brilu")
    tables=getRestaurantsInformation(nameOfRestaurant,"tables")
    table=tables[tableno]
    db.restaurants.update({"_id" : "restaurant"}, {"$push":{str(nameOfRestaurant)+".tables."+str(tableno)+".consumer": consumer_id}},upsert=True);
    return(0)

def updateRestaurantsTablesInformation(nameOfRestaurant,tableno, **kwargs):
    MONGODB_URI = "mongodb://Debangshu:Starrynight.1@ds163694.mlab.com:63694/brilu"
    client = MongoClient(MONGODB_URI, connectTimeoutMS=30000)
    db = client.get_database("brilu")
    tables=getRestaurantsInformation(nameOfRestaurant,"tables")
    table=tables[tableno]
    for key in kwargs:
        table[key]=(kwargs[key])
    db.restaurants.update({"_id" : "restaurant"}, {"$set":{str(nameOfRestaurant)+".tables."+str(tableno): table}},upsert=True);
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

def getConsumerInformation(id,property):
    MONGODB_URI = "mongodb://Debangshu:Starrynight.1@ds163694.mlab.com:63694/brilu"
    client = MongoClient(MONGODB_URI, connectTimeoutMS=30000)
    db = client.get_database("brilu")
    col = db["users"]
    cursor = col.find()
    consumer = cursor[1]
    return(consumer[id][property])



     
    




    
def initializeUser(id,category):
    a=requests.get("https://graph.facebook.com/"+id+"?fields=first_name,last_name,profile_pic&access_token="+ACCESS_TOKEN)
    data=a.json()
    name=data['first_name']
    if category=="waiter":
        updateWaitersInformation(id,name=name,name1="")
    if category=="consumer":
        updateConsumersInformation(id,name=name,name1="")  
@socketio.on('connected')
def handle_my_custom_event(msg):
    print(msg)     
    emit('okrefreshpage', msg)
@socketio.on('connect')
def handleConnect():
    print('yeay connected')
@app.route("/cart/<cartdata>", methods=['GET', 'POST'])

def cart(cartdata):
  if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook."""
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
  else:
    
    print("yea")
    print(cartdata)
    consumer_id=json.loads(cartdata)["id"]
    mycart=json.loads(cartdata)["cart"]

    a=requests.get("https://graph.facebook.com/"+consumer_id+"?fields=first_name,last_name,profile_pic&access_token="+ACCESS_TOKEN)
    data=a.json()
    firstname=data['first_name']
    
         
    print(consumer_id)
    restaurant=getConsumerInformation(consumer_id,"currentRestaurant")
    tableno=getConsumerInformation(consumer_id,"currentTable")
    tables=getRestaurantsInformation(restaurant,"tables")
    table=tables[tableno]
    waiterid=table['waiter']
    updateRestaurantsTablesInformation(restaurant,tableno, whoLastOrdered=consumer_id)     
    send_message(consumer_id, "","","your order is pending!")
    #send_message(waiterid, "","","Table number "+tableno+" has ordered!, the cart is: "+str(mycart))  
    updateRestaurantsCartInformation(restaurant,tableno,**{consumer_id:{"firstname":firstname,"status":"pending","mycart":mycart}})   
    updateRestaurantsStatusInformation(restaurant,tableno,consumer_id, "pending","changeonlybucket")
    cartjsonconsumer={"restaurant":restaurant,"tableno":tableno,"identity":"consumer"}
    cartjsonwaiter={"restaurant":restaurant,"tableno":tableno,"identity":"waiter"}
    cartjsonmanager={"restaurant":restaurant,"tableno":tableno,"identity":"manager"}     
    responseconsumer=   {"recipient":{"id":consumer_id},"message":{"quick_replies": [
      {"content_type":"text","title":"Waiter","payload":'Waiter'}],   
      "attachment":{"type":"template",
          "payload":{"template_type":"generic","elements":[
                 {"title":"Group Order",
                   "image_url":"https://images.homedepot-static.com/productImages/1e1d64ec-a8b2-4328-9588-60d2b13a27e2/svn/yard-carts-cw5024-64_1000.jpg",
                     "subtitle":"See the group order here","buttons":[{ "type": "web_url","url": "https://studmenuweb.herokuapp.com/groupcart/"+json.dumps(cartjsonconsumer),
                 "title": "View Order","messenger_extensions": True}] }]}}}}
    responsewaiter=   {"recipient":{"id":waiterid},"message":{"quick_replies": [
      {"content_type":"text","title":"Waiter","payload":'Waiter'}],   
      "attachment":{"type":"template",
          "payload":{"template_type":"generic","elements":[
                 {"title":"Table number "+tableno,
                   "image_url":"https://images.homedepot-static.com/productImages/1e1d64ec-a8b2-4328-9588-60d2b13a27e2/svn/yard-carts-cw5024-64_1000.jpg",
                     "subtitle":"See the group order here","buttons":[{ "type": "web_url","url": "https://studmenuweb.herokuapp.com/groupcart/"+json.dumps(cartjsonwaiter),
                 "title": "Order","messenger_extensions": True}] }]}}}}     
    r=pay(responseconsumer) 
    r=pay(responsewaiter)      
    return "yes!!!"
@app.route("/checkout/<data>", methods=['GET', 'POST'])

def checkout(data):
     consumer_id=json.loads(data)["tableno"]    
     restaurant=json.loads(data)["restaurant"]
     tableno=json.loads(data)["tableno"] 
     print('yo done bro haha')
         
         
     helpRestaurantCheckout(restaurant,tableno)    
     
     print(data)
     return "yes!!!"
@app.route("/acceptdeny/<data>", methods=['GET', 'POST'])

def acceptdeny(data):
     consumer_id=json.loads(data)["id"]    
     restaurant=json.loads(data)["restaurant"]
     tableno=json.loads(data)["tableno"]  
     acceptdeny=json.loads(data)["acceptdeny"]
     updateRestaurantsStatusInformation(restaurant,tableno,consumer_id, acceptdeny,"changeall")
     datasocket="the socket worked!"
     socketio.emit("okrefreshpage", datasocket, broadcast=True)
     send_message(consumer_id, "","","your order is "+ acceptdeny)
         
     print(data)
     return "yes!!!"
    

if __name__ == "__main__":
     socketio.run(app)     
   
