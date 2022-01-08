import datetime
from django.http.request import HttpHeaders
from django.http import HttpResponse
import requests
import json

from django.http import JsonResponse
from evangelisation.models import Personne


from evangelisation.utils import month_name
from pyfcm import FCMNotification



def send_notification(registration_ids , message_title , message_desc):
    fcm_api = "AAAAJBdk1cg:APA91bGv8-77N2UDAoav7HksTFWNHCkNEFviAKq6e6FdGY9tfG0ZFYPAdnVXbgzhIdf3nw32C1oF3wFGmrD9l57YGDrk7fflXl0G3ODjYkhx619qZbc0puR3SprofgX2BtfJ6xh6SlJ6"
    url = "https://fcm.googleapis.com/fcm/send"
    
    headers = {
    "Content-Type":"application/json",
    "Authorization": 'key='+fcm_api}

    payload = {
        "registration_ids" :registration_ids,
        "priority" : "high",
        "notification" : {
            "body" : message_desc,
            "title" : message_title,
            "image" : "https://i.ytimg.com/vi/m5WUPHRgdOA/hqdefault.jpg?sqp=-oaymwEXCOADEI4CSFryq4qpAwkIARUAAIhCGAE=&rs=AOn4CLDwz-yjKEdwxvKjwMANGk5BedCOXQ",
            "icon": "https://yt3.ggpht.com/ytc/AKedOLSMvoy4DeAVkMSAuiuaBdIGKC7a5Ib75bKzKO3jHg=s900-c-k-c0x00ffffff-no-rj",
            
        }
    }

    result = requests.post(url, data=json.dumps(payload), headers=headers )
    print(result.json())


def send(request):
    resgistration  = [
        "dQ5j6fgAFHXV5-LxS9aVDw:APA91bEzu_JUHqpO89t_7RpAuBXZ7dmwl151MQmFU3pidfZ26EnvsTtre6Ck9dFDyaCkFxpcGPmSeNL9mYfg_l-wPUsQqhUnktlP6TtGWmfn6TuZyTQTUxAjtLg44CIt2Cbmg_hEmNKn"
    ]
    liste_anniv_actuel = list()
    jour_actuel = datetime.date.today().day
    mois_actuel = datetime.date.today().month
    annee_actuel = datetime.date.today().year
    msg_title = f"Anniversaire du **{jour_actuel} {month_name(mois_actuel)}**"

    all_anniv_actuel = Personne.objects.filter(date_naissance__day=jour_actuel, date_naissance__month=mois_actuel)
    for anniv in all_anniv_actuel:
        liste_anniv_actuel.append(anniv.nom_et_prenom)
    if liste_anniv_actuel:
        send_notification(resgistration , msg_title, f'{liste_anniv_actuel}')
    else:
        send_notification(resgistration , msg_title, f"pas d'anniversaire")
    return HttpResponse("sent")




def showFirebaseJS(request):
    data='importScripts("https://www.gstatic.com/firebasejs/9.6.1/firebase-app.js");' \
         'importScripts("https://www.gstatic.com/firebasejs/9.6.1/firebase-messaging.js"); ' \
         'var firebaseConfig = {' \
         '        apiKey: "AIzaSyBk-4j4ID2_R32qf4jxIif0M0qDKYu3YgE",' \
         '        authDomain: "books-b6e0d.firebaseapp.com",' \
         '        databaseURL: "https://books-b6e0d.firebaseio.com",' \
         '        projectId: "books-b6e0d",' \
         '        storageBucket: "books-b6e0d.appspot.com",' \
         '        messagingSenderId: "155011306952",' \
         '        appId: "1:155011306952:web:1f2a9c5b2b7a51b79b5cfd",' \
         '        measurementId: "G-13GWZ275BD"' \
         ' };'\
         'firebase.initializeApp(firebaseConfig);' \
         'const messaging=firebase.messaging();' \
         'messaging.setBackgroundMessageHandler(function (payload) {' \
         '    console.log(payload);' \
         '    const notification=JSON.parse(payload);' \
         '    const notificationOption={' \
         '        body:notification.body,' \
         '        icon:notification.icon' \
         '    };' \
         '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
         '});'

    return HttpResponse(data, content_type="text/javascript")










