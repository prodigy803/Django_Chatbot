import json, requests, random, re
from pprint import pprint

from django.views import generic
from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from textblob import TextBlob
import numpy as np
from wit import Wit

import bottlenose
from bs4 import BeautifulSoup

import pymongo


amazon = bottlenose.Amazon(
   AWSAccessKeyId = 'AKIAI4OEDJ5XO4QXFWHA', AWSSecretAccessKey = '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', AssociateTag = 'theaedifex-21' ,
    Parser=lambda text: BeautifulSoup(text, 'xml')
)

#results = amazon.ItemLookup(ItemId="0198596790", ResponseGroup="SalesRank")


client = Wit('2FMGJOH2YTIVTPA2UJWUD2HDBNZYDDDR')

#from django.views.decorators.csrf import csrf_exempt
# Create your views here.
class YoMamaBotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == '9833467730':
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events 
                if 'message' in message:
                    # Print the message to the terminal
                    #pprint(message)a
                    # Assuming the sender only sends text. Non-text messages like stickers, audio, pictures
                    # are sent as attachments and must be handled accordingly. 
                    post_facebook_message(message['sender']['id'], message['message']['text'])     
        return HttpResponse()
def post_facebook_message(fbid, received_message):           
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAACSDZCKZBGZCsBACrtmqe34TsJZCXJwAy6y2KBYDhS84soZAoYKWlif5XQuxDklThtWgRp2jZAop61F8oac5NkDh838BP30mS2zyM0LCcZC6zJZCV2l5Bsu3ZAnkrw2iddwsjxlrvfvZBjnRDZC9ZBF6hcnnsG8TBhVYkyhlbFL0nQSIAZDZD'
    
    #blob = TextBlob(received_message)
    #list2 = blob.words
    #response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":str(list2)}})

    resp = client.message(received_message)
    main_resp = 'Yay, response: ' + str(resp)
    print(type(resp))
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":main_resp}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())

