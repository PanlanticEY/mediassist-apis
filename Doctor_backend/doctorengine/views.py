
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import symbl
from datetime import datetime
import uuid
import firebase_admin
from firebase_admin import credentials, db
from openai import OpenAI

cred = credentials.Certificate("credentials.json")
#firebase_admin.initialize_app(cred,{"databaseURL": "https://haalo-27946-default-rtdb.firebaseio.com"})
final_messages = ""
connection_Id=''
client = OpenAI(api_key="")
# Create your views here.


def index(request):
    return render(request, 'index.html')

def loading(request):
    return render(request, 'loading.html')

def home(request):

    

    def store_and_print_messages(response):
        global final_messages


        new_messages = [f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message['payload']['content']}" for message in response["messages"]]
        final_messages += "\n".join(new_messages)
        print("Doctor Transcript-> ", final_messages)

    
        ref = db.reference("/")
        connectionRef=ref.child('connectionId')
        connectionRef.set({'currentConnectionId':connection_Id})
        users_ref = ref.child('meetingData')
        meeting_ref=users_ref.child(connection_Id)
        meeting_ref.update({
            'doctorTranscript':final_messages,
        })


        

    def print_live_transcription(response):
        print(
            "live transcription : {}".format(
                response["message"]["punctuated"]["transcript"]
            )
        ) if "punctuated" in response["message"] else print(response)

    events = {
        "message_response": store_and_print_messages,
        "message": print_live_transcription,
    }

    connection_object = symbl.Streaming.start_connection(
        insight_types=["question", "action_item"],
        speaker={"name": "John", "email": "john@example.com"},
    )


    connection_Id='SUxSMTBFNlFIS0xO'
    connection_object.subscribe(events)
    connection_object.send_audio_from_mic()
   
    return render(request,'home.html')
