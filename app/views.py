from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
import random
import requests
from .models import Person, Message, Conversations
from .serializer import PersonSerializer, MessageSerializer, ConversationsSerializer
from revChatGPT.V1 import Chatbot
from OpenAIAuth import Error
import OpenAIAuth

IAM_TOKEN = 't1.9euelZqNnMrLlMuLlJyej5SXmY-Zye3rnpWax5CLmcvOzp6Sk4mNkJWSisjl9PdEHjZe-e99Lk2q3fT3BE0zXvnvfS5Nqg.pduZAmgB4OQFLzsgnFprlRVB7Ze3emwQSJ-icJqEPncIpuO-s2wa1jUswpmb5sq_Rtym_QvN1tQbMUdWhD3jCQ'
folder_id = 'b1glbhukbdjodg7u25t4'
target_language1 = 'en'
target_language2 = 'kk'
access_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJudXJsYW5udXJsYW5vdjYxMkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZX0sImh0dHBzOi8vYXBpLm9wZW5haS5jb20vYXV0aCI6eyJ1c2VyX2lkIjoidXNlci1WTEpZR0h1dGNvV01KbVBzVkM2NUc0UzIifSwiaXNzIjoiaHR0cHM6Ly9hdXRoMC5vcGVuYWkuY29tLyIsInN1YiI6ImF1dGgwfDYzZjA1OWM5YWM3YTY3YzdjOTY2ZTcyOSIsImF1ZCI6WyJodHRwczovL2FwaS5vcGVuYWkuY29tL3YxIiwiaHR0cHM6Ly9vcGVuYWkub3BlbmFpLmF1dGgwYXBwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2ODAzNzE1MzYsImV4cCI6MTY4MTU4MTEzNiwiYXpwIjoiVGRKSWNiZTE2V29USHROOTVueXl3aDVFNHlPbzZJdEciLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIG1vZGVsLnJlYWQgbW9kZWwucmVxdWVzdCBvcmdhbml6YXRpb24ucmVhZCBvZmZsaW5lX2FjY2VzcyJ9.AVvPEdPg13rCAuaTHjLIxHCZs7BVgiN4NpEtK47Vbvv_7cMVCWiru2ktEwo7-fvMkqWC-oo2K83ZRlxnx-k3xVaeIKCOvv_Sgt2EbMZMMrsIRuPlM7EEMd_nJoTa1cyhBGtBCk6KJPA4hUAkZEOsKhZrl5RWV3HlAnt54MZe3UBvvpCkLu7z_PO28TSVuivFpBBw0A_R_9Mb4UFoyWhCABV77reC5nRjPUBitLQjkFMGBDSIMTsGhIWCFL_iPvz2BWKgQG_fVfXlT2mPXDM0m-6_FYsCLGiXhEv4ECywhzzu-KO84D1tHpBbHLnT8PJThQuh4uTZCsG4k--tRw49Zw'
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {IAM_TOKEN}"
}

def translate(text, target_language):
    body = {
        "languageCodeHints":["ru", "en", 'kk'],
        "texts": text,
        "folderId": folder_id,
        "targetLanguageCode": target_language
    }
    trans_response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
        json = body,
        headers = headers
    )
    #print(trans_response.json()['translations'][0]['text'])
    return trans_response.json()['translations'][0]['text']

@api_view(['POST'])
def createPerson(request):
    data = request.data
    try:
        existing_person = Person.objects.get(email=data['email'], password=data['password'])
    except Person.DoesNotExist:
        existing_person = None
    if existing_person:
        serializer = PersonSerializer(existing_person, many=False)
        return Response(serializer.data)
    try:
        chatbot = Chatbot(config={
            'email' : data['email'],#'magzhan200508@gmail.com',
            'password' : data['password']#'Magzhan221549'
        })
        person = Person.objects.create(
        email = data['email'],
        password = data['password'],
        user_c = random.randint(10000000, 99999999)
        )
        serializer = PersonSerializer(person, many = False)
        person.save()
        return Response(serializer.data)
    except Error as e:
        # Check if the error is an OpenAIAuth.Error
        if isinstance(e, OpenAIAuth.Error):
            #print("Wrong password or login")
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Unexpected error'}, status=status.HTTP_403_FORBIDDEN)
    
    

# @api_view(['GET'])
# def getPerson(request, token):
#     person = Person.objects.get(user_c = token)
#     serializer = PersonSerializer(person, many = False)
#     return Response(serializer.data)

@api_view(['GET'])
def getMessages(request, token):
    message = Message.objects.filter(token = token).order_by('-id')
    serializer = MessageSerializer(reversed(message), many=True)
    return Response(serializer.data)

@api_view(['POST'])
def postMessage(request):
    data = request.data
    person = Person.objects.get(user_c = data['token'])
    chatbot = Chatbot(config={
        # 'email' : person.email,#'magzhan200508@gmail.com',
        # 'password' : person.password#'Magzhan221549'
        "access_token":access_token,
    })
    #print(chatbot.get_conversations())
    response = None
    if data['isKazakh']:
        question_in_english = translate(text=data['question'], target_language=target_language1)
    else:
        question_in_english = data['question']
    #print(question_in_english)
    answer = []
    conversation_id = None
    try:
        if data.get('conv_id'):
            conversation_id = data['conv_id']
        for ans in chatbot.ask(prompt=question_in_english, conversation_id=conversation_id):
            response = ans
        answer = response['message'].split('```')
    except Exception as e:
        if e.code:
            return Response({'error': 'Too many requests'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        return Response({'error': 'Сервер переполнен'}, status=status.HTTP_400_BAD_REQUEST)
    
    if data['isKazakh']:
        if len(answer) == 1:
            translation = translate(answer[0], target_language=target_language2)
        else:
            for i in range(0, len(answer), 2):
                answer[i] = translate(text=answer[i], target_language=target_language2)
            translation = '```'.join(answer)
    else:
        if len(answer) == 1:
            translation = translate(answer[0], target_language=target_language2)
        else:
            translation = response
    
    
    if(not conversation_id):
        conversation_id = response['conversation_id']
    message = Message.objects.create(
        token = data['token'],
        question = data['question'],
        isKazakh = data['isKazakh'],
        answer = translation,
        conv_id = conversation_id
        #conversation_id = conversation_id
    )
    serializer = MessageSerializer(message, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def getConversations(request):
    data = request.data
    try:
        chatbot = Chatbot(config={
            # 'email' : data['email'],#'magzhan200508@gmail.com',
            # 'password' : data['password'],#'Magzhan221549'
            "access_token":access_token
        })
    except Exception as e:
        print(e)
        return Response({'error': 'incorrect password or email'}, status=status.HTTP_400_BAD_REQUEST)
    conversations = chatbot.get_conversations()  # get the conversations

    # create a list of Conversation instances
    conversation_instances = [Conversations() for _ in range(len(conversations))]

    # assign the fields to the corresponding Conversation instance
    for i, conv in enumerate(conversations):
        conversation_instances[i].conv_id = conv['id']
        conversation_instances[i].title = conv['title']
    serializer = ConversationsSerializer(conversation_instances, many = True)
    return Response(serializer.data)
    

