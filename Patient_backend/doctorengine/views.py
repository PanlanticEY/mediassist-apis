
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import symbl
from datetime import datetime
import uuid
import firebase_admin
from firebase_admin import credentials, db
from openai import OpenAI

cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred,{"databaseURL": "https://haalo-27946-default-rtdb.firebaseio.com"})
final_messages = ""
connection_Id=''
connectionValue=''
client = OpenAI(api_key="")
# Create your views here.


def index(request):
    return render(request, 'index.html')

def loading(request):
    return render(request, 'loading.html')

def home(request):


    
    ref = db.reference("/")
    users_ref = ref.child('connectionId')

    # Fetch data from Firebase
    data = users_ref.get()
    connectionValue = data.get('currentConnectionId', '')
    

            
    '''print('Firebase Fetched', connectionValue)'''

    

    def store_and_print_messages(response):
        global final_messages
        global doctorSpeech

        doctorSpeech=""

        new_messages = [f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message['payload']['content']}" for message in response["messages"]]
        final_messages += "\n".join(new_messages)
        print("Patient -> ", final_messages)

        'disease prediction'
        

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You will be provided with a conversation between doctor and patient. Your role is to  Generate a list of possible diseases based on the symptoms with probability value which should be strictly a whole number and sum upto 100,   Don't give any other output like Ask doctor for diagnosis etc. Just the prediction based on your output is required. The diseases to be considered for prediction are Flu, Common Cold, Gastroenteritis, Migraine, Pneumonia, Bronchitis, Asthma, Diabetes, Hypertension, Arthritis, Osteoporosis, Alzheimer's Disease, Parkinson's Disease, Cancer, HIV/AIDS, Stroke, Heart Attack, Kidney Stones, Lung Cancer, Breast Cancer, Prostate Cancer, Leukemia, Hepatitis, Malaria, Cholera, Tuberculosis, Ebola, Zika Virus, COVID-19, Chickenpox, Measles, Rubella, Mumps, Whooping Cough, Hepatitis B, Hepatitis C, Influenza, Rheumatoid Arthritis, Epilepsy, Multiple Sclerosis, Psoriasis, Celiac Disease, Ulcerative Colitis, Crohn's Disease, Lupus, Fibromyalgia, Chronic Fatigue Syndrome, Sleep Apnea, Anemia, Gout, Osteoarthritis, Acne, Eczema, Psoriatic Arthritis, Endometriosis, Polycystic Ovary Syndrome (PCOS), Atrial Fibrillation, Cirrhosis, Gallstones, Pancreatitis, Appendicitis, Gastritis, Diverticulitis, Cataracts, Glaucoma, Macular Degeneration, Osteoporosis, Hemorrhoids, Varicose Veins, Achilles Tendonitis, Tennis Elbow, Plantar Fasciitis, Migraine, Cluster Headaches, Concussion, OCD (Obsessive-Compulsive Disorder), PTSD (Post-Traumatic Stress Disorder), Bipolar Disorder, Schizophrenia, Anorexia Nervosa, Bulimia Nervosa, Insomnia, Narcolepsy, Restless Legs Syndrome, Scoliosis, Herniated Disc, Sciatica, Tinnitus, Menopause, Andropause, Hypothyroidism, Hyperthyroidism, Type 1 Diabetes, Type 2 Diabetes, Gestational Diabetes, Alcoholism, Drug Addiction, Nicotine Addiction, Gambling Addiction, Sexual Addiction, Depression, Anxiety, Panic Disorder, Phobias, Postpartum Depression, Seasonal Affective Disorder (SAD), Autism Spectrum Disorder (ASD), ADHD (Attention-Deficit/Hyperactivity Disorder), Dyslexia, Dyspraxia, Down Syndrome, Cerebral Palsy, Fetal Alcohol Syndrome (FAS), Tourette Syndrome, Eating Disorders, Sleep Disorders, Personality Disorders, Developmental Disorders, Dengue Fever, Typhoid Fever, Sinusitis, Tension headache, Obesity, Osteomyelitis, Peptic Ulcer, Gastroesophageal Reflux Disease (GERD), Hemochromatosis, Huntington's Disease, Hyperlipidemia, Hypoglycemia, Irritable Bowel Syndrome (IBS), Jaundice, Lactose Intolerance, Melanoma, Myocardial Infarction, Narcolepsy, Nephrolithiasis, Otitis Media, Pancreatic Cancer, Pelvic Inflammatory Disease (PID), Polycythemia Vera, Prostatitis, Pulmonary Embolism, Retinoblastoma, Sarcoidosis, Sepsis, Septic Arthritis, Shingles (Herpes Zoster), Sickle Cell Disease, Spinal Stenosis, Temporomandibular Joint Disorder (TMJ), Testicular Cancer, Thalassemia, Thoracic Outlet Syndrome, Tonsillitis, Toxoplasmosis, Trichomoniasis, Ulcerative Colitis, Urethritis, Urolithiasis, Uterine Fibroids, Vaginitis, Vasculitis, Vitiligo, Vulvodynia, Wilson's Disease, Yellow Fever, Zollinger-Ellison Syndrome, Acromegaly, Adenomyosis, Asbestosis, Behcet's Disease, Bursitis, Chlamydia, Coeliac Disease, Cystic Fibrosis, Dermatitis, Dermatofibroma, Diverticulosis, Endocarditis, Fibromyalgia, Gastroparesis, Graves' Disease, Guillain-Barre Syndrome, Hantavirus Pulmonary Syndrome, Hirschsprung's Disease, Huntington's Disease, Hydrocephalus, Interstitial Cystitis, Kawasaki Disease, Lichen Planus, Lipoma, Lymphedema, Marfan Syndrome, Meningitis, Myasthenia Gravis, Osteomalacia, Paget's Disease of Bone, Porphyria, Prader-Willi Syndrome, Reactive Arthritis, Reye's Syndrome, Rickets, Sjogren's Syndrome, Strep Throat, Turner Syndrome, Wegener's Granulomatosis, Wilms Tumor, Xeroderma Pigmentosum. No other diseases should be considered. "},
                {"role": "user", "content": 'Patient Transcript: '+ final_messages + 'Doctor Transcript: ' + doctorSpeech}
            ],
        
    
        )
        diseasePrediction=completion.choices[0].message.content
        print(diseasePrediction)

        'Prescription Suggestion'
        

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You will be provided with a conversation between doctor and patient.   Your role is to provide general medicine prescription which are used in India based on the possible diseases derived from symptoms. Don't give any other output like Ask doctor for diagnosis etc. "},
                {"role": "user", "content": 'Patient Transcript: '+ final_messages + 'Doctor Transcript: ' + doctorSpeech}
            ],
        
    
        )
        prescription=completion.choices[0].message.content
        print(prescription)

        'Prompt Suggestion'
        

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You will be provided with a conversation between doctor and patient. Your role is To provide question suggestions for the doctor so that he can ask patient . Don't give any other output like Ask doctor for diagnosis etc. Just the prediction based on your output is required. "},
                {"role": "user", "content": 'Patient Transcript: '+ final_messages + 'Doctor Transcript: ' + doctorSpeech}
            ],
        
    
        )
        prompt=completion.choices[0].message.content
        print(prompt)




        print('Fetched from DB',doctorSpeech)

        ref = db.reference("/")
        users_ref = ref.child('connectionId')

        # Fetch data from Firebase
        data = users_ref.get()
        connectionValue = data.get('currentConnectionId', '')

       
        value_ref=ref.child('meetingData')
        meeting_ref = value_ref.child(connectionValue)

        # Fetch data from Firebase
        data = meeting_ref.get()
        doctorSpeech = data.get('doctorTranscript', '')
        
        

        
        value_ref=ref.child('meetingData')
        meeting_ref = value_ref.child(connectionValue)
        meeting_ref.update({
            'disease':diseasePrediction,
            'patientTranscript':final_messages,
            'prompt':prompt,
            'prescription':prescription,

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


    
    connection_object.subscribe(events)
    connection_object.send_audio_from_mic()
   
    return render(request,'home.html')
