 #Python libraries that we need to import for our bot
import random
from pymongo import MongoClient
from flask import Flask, request,render_template
from pymessenger.bot import Bot
import os

import requests
import urllib
from flask_cors import CORS
import json
from decisionTree import decision,listOfExams,askQuestion,handleResults,decisionRightWrong
from intelligence import BRAIN
import time
app = Flask(__name__)
CORS(app)

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


@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
       
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
                            send_message(secretcode[1],"a","a","Congrats your request has been accepted! :)")
                             
                            #pushRestaurantsWaitersInformation(restaurant,id,secretcode[3])        
                            return "Message Processed"
                      if secretcode.find('TableChangeDeny') != -1:
                            secretcode=secretcode.split('|')
                            send_message(secretcode[1],"a","a","Sorry the waiter has not accepted your table number :(")
                            return "Message Processed"
                    topic,mood,response = get_message(recipient_id,message['message'].get('text'))
                    isQuickReply=checkQuickReply(message['message'].get('text'),recipient_id)
                    
                    #isQuickReplyHint=checkQuickReply(response,recipient_id,name,restaurant,tableno)
                    if isQuickReply==False  :
                        restaurant=getConsumerInformation(recipient_id,"currentRestaurant")
                        tableno=getConsumerInformation(recipient_id,"currentTable")
                        tables=getRestaurantsInformation(restaurant,"tables")
                        table=tables[tableno]
                        waiterid=table['waiter'] 
                        a=requests.get("https://graph.facebook.com/"+waiterid+"?fields=first_name,last_name,profile_pic&access_token="+ACCESS_TOKEN)
                        data=a.json()
                        firstname=data['first_name']  
                        msg=message['message'].get('text')
                        question=['Is there stag entry?','Are stags allowed?','Is there couple entry?','Opening time?','Closing time?','What kind of music is today?','Music?','Who is the DJ?','Do you have brewed beers?','Book a table','Offers','Happy hours','Happy hours timing?']
                        answer=['Yes, why not','Sorry, we are taking only couple entry today','Yes, we are taking only couple entry today','We start pouring at 6 pm','We have bollywood night today.','We have bollywood night today.','We have Marshmello playing today.','Yes, we have lot of them. Please take a look at our menu.','Sure, how many of you are coming to the party?','Here are some of the fantastic offers today','Our happy hours are 4pm to 7pm','Our happy hours are 4pm to 7pm']
                        for i in range(0,len(question)):
                            if msg==question[i]:
                              send_message(recipient_id,"a","a",answer[i])
                              return "Message Processed"
                        send_message(waiterid,"a","a","Table No. "+tableno+": "+message['message'].get('text'))  
                        send_message(recipient_id,"a","a","(y)")
                        #instruction="Looks like you typed something 🙄 \n"
                        #send_message(recipient_id,"a","a",instruction)
                        #time.sleep(1)
                        #instruction2="Please use buttons or quick replies only. "   
                        #send_message(recipient_id,"a","a",instruction2)
                        
                        #instruction3="Try this:"+ "\n"+ "-To open menu tap Menu"+"\n"+"-To call steward tap Steward"
                        #button= [{ "type": "web_url","url": "https://reliable-plasma-234606.appspot.com/menu/"+getConsumerInformation(recipient_id,"currentRestaurant"),
                        #"title": "Menu","messenger_extensions": True},
                        #{"type":"postback","title":"Steward","payload":"Steward"}] 
                        #bot.send_button_message(recipient_id,instruction3,button) 
                        return "Message Processed"
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    response = ['(y)',':)',":D"]
                    
                    quickreply(recipient_id,['Call Steward'],random.choice(response))
               
    return "Message Processed"


def verify_fb_token(token_sent):
  
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
  print(result)       
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
      if fulladdress[0]=='R':
         friendId=fulladdress[1:]
         selfId=id
         send_message(id,'a','a', "Congracts!! you will get 20% discount on your next visit to cad")
         send_message(friendId,'a','a', "Get 20% discount when your friend visits CAD next time") 
         return "success" 
      fulladdress=fulladdress.split("_")
      if(fulladdress[0] == "visitingCard"):
                  
            welcomeVisitor="Hi "+ name+ "!!"+"\n"+"\n"      
            send_message(id,'a','a', welcomeVisitor)  
            #typingon=pay({"recipient":{"id":id},"sender_action":"typing_on"})
            time.sleep(1)
            first_message="Eating out is something you love to do but figuring out what to eat when you go to a nice restaurant is often an issue. Right?"      
            send_message(id,'a','a', first_message) 
            #typingon=pay({"recipient":{"id":id},"sender_action":"typing_on"})
            time.sleep(2)     
            second_message="Meallion makes you preview your meals visually, swiftly by just tapping on the menu right on this messenger. B) "      
            send_message(id,'a','a', second_message)
            #typingon=pay({"recipient":{"id":id},"sender_action":"typing_on"})
            time.sleep(2)      
            third_message="EGG-cited to know more? :D "      
            send_message(id,'a','a', third_message)  
            #typingon=pay({"recipient":{"id":id},"sender_action":"typing_on"})
            time.sleep(1)    
            #fourth_message="Contact Seemant@8101443644/ or Debangshu@7384342412"      
            #send_message(id,'a','a', fourth_message) 
            responseVisitor=   {"recipient":{"id":id},"message":{   
            "attachment":{"type":"template","payload":{"template_type":"generic","elements":[
            {"title":"Seemant Jay","image_url":"https://storage.googleapis.com/meallionpics/General/Visiting%20Card/Seemant.png",
            "subtitle":"CEO @ Meallion","buttons":[{"type":"phone_number","title":"Call Seemant","payload":"+918101443644"}]},
            {"title":"Debangshu Paul","image_url":"https://storage.googleapis.com/meallionpics/General/Visiting%20Card/DebangshuPaul.jpg",
            "subtitle":"CTO @ Meallion","buttons":[{"type":"phone_number","title":"Call Debangshu","payload":"+917384342412"}]}         
            ]}}}}   
            r=pay(responseVisitor)       
            return "success"      
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
         if(fulladdress[0]=="visitingCard"):
            welcomeVisitor="Hi "+ name+ "!!"+"\n"+"\n"      
            send_message(id,'a','a', welcomeVisitor)  
            #typingon=pay({"recipient":{"id":id},"sender_action":"typing_on"})
            time.sleep(1)
            first_message="Eating out is something you love to do but figuring out what to eat when you go to a nice restaurant is often an issue. Right?"      
            send_message(id,'a','a', first_message) 
            #typingon=pay({"recipient":{"id":id},"sender_action":"typing_on"})
            time.sleep(2)     
            second_message="Meallion makes you preview your meals visually, swiftly by just tapping on the menu right on this messenger. B) "      
            send_message(id,'a','a', second_message)
            #typingon=pay({"recipient":{"id":id},"sender_action":"typing_on"})
            time.sleep(2)      
            third_message="EGG-cited to know more? :D "      
            send_message(id,'a','a', third_message)  
            #typingon=pay({"recipient":{"id":id},"sender_action":"typing_on"})
            time.sleep(1)     
                  
            #fourth_message="Contact Seemant@8101443644/ or Debangshu@7384342412"      
            #send_message(id,'a','a', fourth_message) 
            responseVisitor=   {"recipient":{"id":id},"message":{   
            "attachment":{"type":"template","payload":{"template_type":"generic","elements":[
            {"title":"Seemant Jay","image_url":"https://storage.googleapis.com/meallionpics/General/Visiting%20Card/Seemant.png",
            "subtitle":"CEO @ Meallion","buttons":[{"type":"phone_number","title":"Call Seemant","payload":"+918101443644"}]},
            {"title":"Debangshu Paul","image_url":"https://storage.googleapis.com/meallionpics/General/Visiting%20Card/DebangshuPaul.jpg",
            "subtitle":"CTO @ Meallion","buttons":[{"type":"phone_number","title":"Call Debangshu","payload":"+917384342412"}]}         
            ]}}}}   
            r=pay(responseVisitor) 
            return "success"         
         restaurant=fulladdress[0]
         try:   
           tableno=fulladdress[1]
         except:
            tableno="none"    
         
         handleUser(id,fulladdress,name,restaurant,tableno)  
       else:
         welcome="please scan the QR code infront of you!"
         send_message(id,'a','a', welcome)  
    if output['entry'][0]['messaging'][0]['postback']['payload']=='Steward':
 
        quickreply(id,["Water","Cutlery","Napkins","Bill","Call Steward"],"How may he help you?")
        #return 'success'
    if output['entry'][0]['messaging'][0]['postback']['payload']=='Good':
        send_message(id,'a','a','I am glad :) \n Refer your friend and earn discount on your next visit to this restaurant') 
        bot.send_button_message(id,'Share',[shareme(id)])
        
        #return 'success'
    if output['entry'][0]['messaging'][0]['postback']['payload']=='Okayish':
        send_message(id,'a','a','We would like to improve in future ') 
        send_message(id,'a','a',' Meanwhile ou can share your friend and get amazing discount on your next visit :D') 
        bot.send_button_message(id,'Share',[shareme(id)])
        #return 'success'
    if output['entry'][0]['messaging'][0]['postback']['payload']=='Bad':
        send_message(id,'a','a','Sorry to hear that \n Please type in what we did wrong ') 
        #return 'success'
     
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
      
       updateConsumersInformation(id,name=name,currentRestaurant=restaurant,currentTable=tableno)  
       updateRestaurantsTablesConsumerInformation(restaurant,tableno, name,id)
       restaurant=getConsumerInformation(id,"currentRestaurant")
       tableno=getConsumerInformation(id,"currentTable")
       tables=getRestaurantsInformation(restaurant,"tables")
       table=tables[tableno]
       waiterid=table['waiter']
       waiter=getRestaurantsInformation(restaurant,"waiters")  
       yourwaiter=waiter[waiterid]["name"]  
       welcome='Hi! '+name+",\n"+"\n"+"Welcome to "+restaurant+" :) \n  \n"+"Our steward "+ yourwaiter+" will be serving your Table "+tableno
       send_message(id,'a','a', welcome)  
         
       instruction="Instructions:"+ "\n"+ "-To open menu tap Menu"+"\n"+"-To call "+yourwaiter+" tap Steward"
       button= [{ "type": "web_url","url": "https://reliable-plasma-234606.appspot.com/menu/"+getConsumerInformation(id,"currentRestaurant"),
                 "title": "Menu","messenger_extensions": True},
               {"type":"postback","title":"Steward","payload":"Steward"}] 
       bot.send_button_message(id,instruction,button) 
       time.sleep(3)
       send_message(id, "","","**After the customer dines")
       send_message(id, "","","It was great hosting you")
       #quickreplyDifferentPayload(idToSend[0],['1','2','3','4','5'],['rating1','rating2','rating3','rating4','rating5'],'Please rate our service')
       button= [{"type":"postback","title":"Good","payload":"Good"},
                {"type":"postback","title":"Okayish","payload":"Okayish"},
                {"type":"postback","title":"Bad","payload":"Bad"}] 
       bot.send_button_message(id,'How was our service?',button) 
       time.sleep(0.7)
       send_message(id, "","","**After feedback,referral")
       
       send_message(id,'a','a','I am glad :) \n Refer your friend and earn discount on your next visit to this restaurant') 
       bot.send_button_message(id,'Share',[shareme(id)])
       
       updateConsumersInformation(id,name=name,currentRestaurant=restaurant,currentTable=tableno)  
def executeWaiterCode(id,fulladdress,name,restaurant,tableno):
    if tableno=="none":
      send_message(id,"a","a","Hi "+name+"!"+"\n"+"Welcome on-board to "+restaurant)
      updateWaitersInformation(id,name=name,currentRestaurant=restaurant,tableno=tableno) 
      info={"name":name,"picurl":"","active":True,"activetables":[]}   
      updateRestaurantsWaitersInformation(restaurant, **{id:info})  
    else:    
      table=getRestaurantsTableInformation(restaurant,tableno) 
      #if table['waiter']=="":
      updateRestaurantsTablesInformation(restaurant,tableno, waiter=id)
      send_message(id,"a","a","On-boarded Table No. :"+tableno)
            
      #else:
      #  send_message(id,"a","a","Waiting for previous Steward's approval")
        
      #  prompt=name+" Wants to on-board your Table No. "+ tableno
         
      #  quickreplyDifferentPayload(table['waiter'],['Accept','Deny'],['TableChangeAccept | '+str(id)+'|'+str(restaurant)+'|'+str(tableno),'TableChangeDeny |'+str(id)],prompt)
        #updateWaitersInformation(id,currentTable=tableno)
    
    
def checkQuickReply(text,id): 
           restaurant=getConsumerInformation(id,"currentRestaurant")
           tableno=getConsumerInformation(id,"currentTable")
           tables=getRestaurantsInformation(restaurant,"tables")
           table=tables[tableno]
           waiterid=table['waiter'] 
           a=requests.get("https://graph.facebook.com/"+waiterid+"?fields=first_name,last_name,profile_pic&access_token="+ACCESS_TOKEN)
           data=a.json()
           firstname=data['first_name']       
                         
           
           if text=="Napkins":
               send_message(waiterid,"a","a"," Table "+ tableno+" :  Napkins")
               button= [{ "type": "web_url","url":  "https://reliable-plasma-234606.appspot.com/menu/"+getConsumerInformation(id,"currentRestaurant"),"messenger_extensions":True, "title": "Menu" },
               {"type":"postback","title":"Steward","payload":"Steward"}] 
               bot.send_button_message(id,'Got it! B) \n'+firstname+' is on the way with napkins. ',button) 
               return True
           if text=="Bill":
               send_message(waiterid,"a","a"," Table "+ tableno+" :  Bill")
               button= [{ "type": "web_url","url":  "https://reliable-plasma-234606.appspot.com/menu/"+getConsumerInformation(id,"currentRestaurant"),"messenger_extensions":True, "title": "Menu" },
               {"type":"postback","title":"Steward","payload":"Steward"}] 
               bot.send_button_message(id,'Got it! B) \n'+firstname+' is on the way with bill.',button) 
               return True
           if text=="Cutlery":
               send_message(waiterid,"a","a"," Table "+ tableno+" : Cutlery")
               button= [{ "type": "web_url","url":  "https://reliable-plasma-234606.appspot.com/menu/"+getConsumerInformation(id,"currentRestaurant"),"messenger_extensions":True, "title": "Menu" },
               {"type":"postback","title":"Steward","payload":"Steward"}] 
               bot.send_button_message(id,'Got it! B) \n'+firstname+' is on the way with cutlery. ',button) 
               return True
           if text=="Water":
               send_message(waiterid,"a","a"," Table "+ tableno+" : Water")
               button= [{ "type": "web_url","url":  "https://reliable-plasma-234606.appspot.com/menu/"+getConsumerInformation(id,"currentRestaurant"),"messenger_extensions":True, "title": "Menu" },
               {"type":"postback","title":"Steward","payload":"Steward"}] 
               bot.send_button_message(id,'Got it! B) \n'+firstname+' is on the way with water. ',button) 
               return True 
           if text=="Call Steward":
               send_message(waiterid,"a","a"," Table "+ tableno+" :  Wants to talk")
               button= [{ "type": "web_url","url":  "https://reliable-plasma-234606.appspot.com/menu/"+getConsumerInformation(id,"currentRestaurant"),"messenger_extensions": True, "title": "Menu" },
               {"type":"postback","title":"Steward","payload":"Steward"}] 
               bot.send_button_message(id,'Got it! B) \n'+firstname+' is on the way. ',button) 
               return True 
           if text=="Accept Order":
               #send_message(waiterid,"a","a"," table number"+ tableno+"is asking for water")
               button= [{ "type": "web_url","url":  "https://reliable-plasma-234606.appspot.com/menu/"+getConsumerInformation(id,"currentRestaurant"),"messenger_extensions":True, "title": "Menu" },
               {"type":"postback","title":"Steward","payload":"Steward"}] 
               bot.send_button_message(id,'Your ordered is accepted :D ',button) 
               time.sleep(1)
               randompic=random.randint(1,50)  
               send_message(id,'a','a', "Hey Meallionaire,you just got a free pun 😀 ") 
               responseimage={"recipient":{"id":id},
               "message":{"attachment":{"type":"image", "payload":{
               "url":"https://storage.googleapis.com/meallionpics/General/Puns/"+str(randompic)+".jpg"}}}}
               r=pay(responseimage)
               return True 
           if text=="Deny Order":
               #send_message(waiterid,"a","a"," table number"+ tableno+"is asking for water")
               button= [{ "type": "web_url","url":  "https://reliable-plasma-234606.appspot.com/menu/"+getConsumerInformation(id,"currentRestaurant"),"messenger_extensions":True, "title": "Menu" },
               {"type":"postback","title":"Steward","payload":"Steward"}] 
               bot.send_button_message(id,'Sorry, your order has been denied :( ',button) 
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
    #db.restaurants.update({"_id" : "restaurant"}, {"$push":{str(restaurant)+".waiters."+str(ID)+".activetables": tableno}},upsert=True);
                
    for key in kwargs:
        db.users.update({"_id" : "waiter"}, {"$set":{str(ID)+"."+str(key): kwargs[key]}},upsert=True);
    
    return(0)
def shareme(id):
    shareit={"type": "element_share","share_contents": { 
    "attachment": {"type": "template",
      "payload": {"template_type": "generic",
        "elements": [{
            "title": "Get amazing discount on your next visit to CAD!!",
            "subtitle": " Upto 20%",
            "image_url": "https://grapevineonline.in/wp-content/uploads/2017/06/Screen-Shot-2017-06-07-at-5.10.10-PM.png?fbclid=IwAR2FgQ1C-Zy3giFrPATUqi2LbHNe-L8vfGCqaqqeQrKXQOIGedRcP40ORmA",
            "default_action": {"type": "web_url","url": "https://www.messenger.com/t/MeallionBot"},
            "buttons": [
              {"type": "web_url","url": "https://www.messenger.com/t/MeallionBot?ref=R"+id, "title": "Activate Offer!"
              }]}]}}}}
    return shareit   
def pushRestaurantsWaitersInformation(restaurant, id,tableno):
    MONGODB_URI = "mongodb://Debangshu:Starrynight.1@ds163694.mlab.com:63694/brilu"
    client = MongoClient(MONGODB_URI, connectTimeoutMS=30000)
    db = client.get_database("brilu")
    col = db["restaurants"]
    cursor = col.find()
    restaurant = cursor[0]
    db.restaurants.update({"_id" : "restaurant"}, {"$push":{str(restaurant)+".waiters."+str(id)+".activetables": tableno}},upsert=True);
           
         
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
        waiters[key]=kwargs[key]
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
def updateRestaurantsTablesConsumerInformation(nameOfRestaurant,tableno, name,consumer_id):
    MONGODB_URI = "mongodb://Debangshu:Starrynight.1@ds163694.mlab.com:63694/brilu"
    client = MongoClient(MONGODB_URI, connectTimeoutMS=30000)
    db = client.get_database("brilu")
    tables=getRestaurantsInformation(nameOfRestaurant,"tables")
    table=tables[tableno]
    db.restaurants.update({"_id" : "restaurant"}, {"$push":{str(nameOfRestaurant)+".tables."+str(tableno)+".consumer":{consumer_id:name}}},upsert=True);
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

@app.route("/cart/<cartdata>", methods=['GET', 'POST'])

def cart(cartdata):
 
    
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
    send_message(consumer_id, "a","a","Your order is pending!")
    #send_message(waiterid, "","","Table number "+tableno+" has ordered!, the cart is: "+str(mycart))  
    updateRestaurantsCartInformation(restaurant,tableno,**{consumer_id:{"firstname":firstname,"status":"pending","mycart":mycart}})   
    updateRestaurantsStatusInformation(restaurant,tableno,consumer_id, "pending","changeonlybucket")
    cartjsonconsumer={"restaurant":restaurant,"tableno":tableno,"identity":"consumer"}
    cartjsonwaiter={"restaurant":restaurant,"tableno":tableno,"identity":"waiter"}
    cartjsonmanager={"restaurant":restaurant,"tableno":tableno,"identity":"manager"}     
    responseconsumer=   {"recipient":{"id":consumer_id},"message":{"quick_replies": [
      {"content_type":"text","title":"Call Steward","payload":'Call Steward'}],   
      "attachment":{"type":"template",
          "payload":{"template_type":"generic","elements":[
                 {"title":"Group Order",
                   "image_url":"https://storage.googleapis.com/meallionpics/General/Icons/cheers.jpg",
                     "subtitle":"See the group order here","buttons":[{ "type": "web_url","url": "https://studmenuweb.herokuapp.com/groupcart/"+json.dumps(cartjsonconsumer),
                 "title": "View Order","messenger_extensions": True},{ "type": "web_url","url": "https://reliable-plasma-234606.appspot.com/menu/"+getConsumerInformation(consumer_id,"currentRestaurant"),
                 "title": "Menu","messenger_extensions": True}] }]}}}}
      
    button= [{ "type": "web_url","url": "https://studmenuweb.herokuapp.com/groupcart/"+json.dumps(cartjsonwaiter),
                 "title": "View Order","messenger_extensions": True}] 
    bot.send_button_message(waiterid,'Table: '+tableno,button) 
    r=pay(responseconsumer) 
     
    return "yes!!!"
@app.route("/checkout/<data>", methods=['GET', 'POST'])

def checkout(data):
     consumer_id=json.loads(data)["tableno"]    
     restaurant=json.loads(data)["restaurant"]
     tableno=json.loads(data)["tableno"] 
      
     tableInfo=getRestaurantsTableInformation(restaurant,tableno)
     consumerData=tableInfo['consumer']
     print('consumer data is ',consumerData)
     for consumer in consumerData:
        idToSend=list(consumer.keys())
        send_message(idToSend[0], "","","You have been checked out!")
        #quickreplyDifferentPayload(idToSend[0],['1','2','3','4','5'],['rating1','rating2','rating3','rating4','rating5'],'Please rate our service')
        button= [{"type":"postback","title":"Good","payload":"Good"},
                {"type":"postback","title":"Okayish","payload":"Okayish"},
                {"type":"postback","title":"Bad","payload":"Bad"}] 
        bot.send_button_message(idToSend[0],'How was our service?',button) 
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
     
     send_message(consumer_id, "","","Your order is "+ acceptdeny+" :)")
         
     print(data)
     return "yes!!!"
    

if __name__ == "__main__":
     app.run()    
   
