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
                    sendVideo(recipient_id,'http://clips.vorwaerts-gmbh.de/big_buck_bunny.mp4')
                    quickreply(recipient_id,['Lets test', 'I am Bored!'],random.choice(response))
                """try:
                    dummy=getUserInformation(recipient_id,'name')
                except:
                    initializeUser(recipient_id)"""
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
      tableno=fulladdress[1]    
      welcome='Welcome!'+name+" you are sitting in restaurant "+restaurant+" in table number "+ tableno+" I am your host today :)"
      instruction="To open menu press Open Menu, To call the waiter press Call Waiter"
      send_message(id,'a','a', welcome)
      quickreply(id,['Open Menu','Call Waiter'],instruction)
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
         tableno=fulladdress[1]   
         welcome='Welcome!'+name+" you are sitting in restaurant "+restaurant+" in table number "+ tableno+" I am your host today :)"
       else:
        welcome="Welcome! "+name+" please open the camera and long press to scan the QR code!"
       send_message(id,'a','a', welcome)
       instruction="To open menu press Open Menu, To call the waiter press Call Waiter"
       #initializeUser(id) 
       quickreply(id,['Open Menu','Call Waiter'],instruction)
        
      
def checkCalculator(id,text):
   try:
     text=text.lower()
     text=text.replace('+','%2B')
     text=text.replace("what is","")
     text=text.replace("calculate","")
     text=text.replace("evaluate","")   
     resultOfCalculation=requests.get("http://api.mathjs.org/v4/?expr="+str(text)) 
     if str(resultOfCalculation)=="<Response [200]>":   
      if getUserInformation(id,'insidequestion')==True: 
         p=sendLastOptionsQuickReply(id,resultOfCalculation.text)
         return True
      else:
         quickreply(id,['Lets test', 'I am Bored!'],resultOfCalculation.text)   
         return True
     else:
        return False
    
   
   except:
    return False
    
def checkQuickReply(text,id): 
         try: 
           msges,listofitems=decision(text)
           if text=="Call Waiter":
             quickreply(id,["napkins","spoon","water","Talk to waiter","Open Menu"],"calling waiter what do you want") 
             return True
            if text=="Open Menu": 
                 response=[
                             {
                "type":"web_url",
                "url":"http://www.google.com",
                "title":"Open Menu!",
                "webview_height_ratio": "tall"  
              } ]
                 bot.send_button_message(id,'To open menu press Open Menu ',response)
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

def updateUsersInformation(ID, **kwargs):
    MONGODB_URI = "mongodb://Debangshu:Starrynight.1@ds239055.mlab.com:39055/studmenu"
    client = MongoClient(MONGODB_URI, connectTimeoutMS=30000)
    db = client.get_database("studmenu")
    for key in kwargs:
        db.userInfo.update({"_id" : "5c4e064ffb6fc05326ad8c57"}, {"$set":{str(ID)+"."+str(key): kwargs[key]}},upsert=True);
    return(0)
def getUserInformation(id,property):
    MONGODB_URI = "mongodb://Debangshu:Starrynight.1@ds239055.mlab.com:39055/studmenu"
    client = MongoClient(MONGODB_URI, connectTimeoutMS=30000)
    db = client.get_database("studmenu")
    col = db["userInfo"]
    cursor = col.find()
    userInfo = cursor[0]
    return(userInfo[id][property])

def search_gif(text):
    #get a GIF that is similar to text sent
    payload = {'s': text, 'api_key': '8uWKU7YtJ4bIzYcAnjRVov8poEHCCj8l'}
    r = requests.get('http://api.giphy.com/v1/gifs/translate', params=payload)
    r = r.json()
    url = r['data']['images']['original']['url']
    return url
def send_gif_message(recipient_id, message):
    gif_url = search_gif(message)
    data = json.dumps({"recipient": {"id": recipient_id},"message": {"attachment": {"type": "image","payload": {"url": gif_url}}}})
    params = {"access_token": ACCESS_TOKEN }
    headers = {"Content-Type": "application/json"}
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
def sendLastOptionsQuickReply(id,text):
    options=getUserInformation(id,'lastOptions')
    right=getUserInformation(id,'lastRightAnswer')
    exceeded=getUserInformation(id,'lastExceeded')
    solution=""
    if exceeded==False:
      payload = {"recipient": {"id": id}, "message": {"text":text,"quick_replies": [] }}
      for item in options:
        if item==right:
           payload['message']['quick_replies'].append({"content_type":"text","title":str(item),"payload":'right'})
           
        else:
           payload['message']['quick_replies'].append({"content_type":"text","title":str(item),"payload":'wrong'})
      #payload['message']['quick_replies'].append({"content_type":"text","title":"Give me a hint!","payload":hint})   
      pay(payload)
      return 'success'
    if exceeded==True:
         shortOptions=['A','B','C','D']
         payload = {"recipient": {"id": id}, "message": {"text":text,"quick_replies": []}}
         for itemindex in range(0,4):
            if options[itemindex]==right:
              payload['message']['quick_replies'].append({"content_type":"text","title":shortOptions[itemindex],"payload":'right'})
              
            else:
              payload['message']['quick_replies'].append({"content_type":"text","title":shortOptions[itemindex],"payload":'wrong'})
         #payload['message']['quick_replies'].append({"content_type":"text","title":"Give me a hint!","payload":hint})    
         pay(payload)
    return 'succeeded'        
    
def shareme(message):
    shareit={
     "type": "element_share",
     "share_contents": { 
    "attachment": {
      "type": "template",
      "payload": {
        "template_type": "generic",
        "elements": [
          {
            "title": "I was just answering Brilu's questions!!",
            "subtitle": "He says: " + message,
            #"image_url": "<IMAGE_URL_TO_DISPLAY>",
            "default_action": {
              "type": "web_url",
              "url": "https://www.messenger.com/t/teacherchatbot"
            },
            "buttons": [
              {
                "type": "web_url",
                "url": "https://www.messenger.com/t/teacherchatbot", 
                "title": "Chat now"
              }]}]}}}}
    return shareit
def sendSuperTopic(id):
    response=   {
     "recipient":{"id":id},
     "message":{
      "quick_replies": [
      {
        "content_type":"text",
        "title":"I am Bored!",
        "payload":'I am Bored!'
      }],   
      "attachment":{
        "type":"template",
          "payload":{
           "template_type":"generic",
             "elements":[
                 
                 {
                 "title":"Job Preparation",
                   "image_url":"http://www.dvc.edu/enrollment/career-employment/images/Jobs.jpg",
                      "subtitle":"practice problems that makes you ready for interview I have aptitude,verbal ability and logical reasoning",
                       
                           "buttons":[
                             {"type":"postback",
  "title":"Start now",
  "payload":"jobPrep"},shareme('he helps practice interview questions,you should try it')] },
                 
                 
                 
                  {
                 "title":"class10",
                   "image_url":"http://2.bp.blogspot.com/_Q_ZJiaCqn38/TFIu3dkYfxI/AAAAAAAAACo/63Vuzi-IG4A/s1600/SCIENCE.png",
                     "subtitle":"practice science problems from class 10 and improve your concepts",
                        
                           "buttons":[
                             {"type":"postback",
  "title":"Start now",
  "payload":"class10"},shareme('he helps practice class 10 questions,you should try it')] }
             
             
             
             
             
             
             
             
             
             
             
             ]}}}}
    r=pay(response)
    return r

def sendResult(id, gif,message):
    url = search_gif(gif)
    share=shareme(message)
    response=   {
     "recipient":{
           "id":id
                      },
     "message":{
      "quick_replies": [
      {
        "content_type":"text",
        "title":"Go Back",
        
        "payload":"Go Back"
      },
      {
        "content_type":"text",
        "title":"Continue",
        "payload":"Continue"
      },
        {
        "content_type":"text",
        "title":"I am Bored!",
        "payload":'I am Bored!'
      }
    ],   
      "attachment":{
        "type":"template",
          "payload":{
           "template_type":"generic",
             "elements":[
                 {
                 "title":"Here is your result!",
                   #"image_url":https://images.pexels.com/photos/1642883/pexels-photo-1642883.jpeg?cs=srgb&dl=adults-affection-couple-1642883.jpg&fm=jpg,
                     "subtitle":message,
                        "default_action": {
                            "type":"web_url",
                            "url":"http://brilu.herokuapp.com/result/"+str(id),
                            "webview_height_ratio": "tall"  
                              },
                           "buttons":[
                             {
                "type":"web_url",
                "url":"http://brilu.herokuapp.com/result/"+str(id),
                "title":"See Details!",
                "webview_height_ratio": "tall"  
              },share ] }]}}}}
    
    r=pay(response)
    return r
@app.route("/result/<id>", methods=['GET', 'POST'])
def result(id):
        return render_template('chart.html')
    
def initializeUser(id):
    a=requests.get("https://graph.facebook.com/"+id+"?fields=first_name,last_name,profile_pic&access_token="+ACCESS_TOKEN)
    data=a.json()
    name=data['first_name']
    updateUsersInformation(id,name=name)
    

if __name__ == "__main__":
    app.run()
