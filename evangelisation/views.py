import datetime
from django.http.request import HttpHeaders
from django.http import HttpResponse
import requests
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelformset_factory
from django.http import JsonResponse
from django.http.response import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from evangelisation.forms import PersonneForm, FormNbre
from evangelisation.models import Personne


from evangelisation.utils import month_name
from evangelisation.send_notification import send
from pyfcm import FCMNotification

from pushbullet import Pushbullet


@login_required(login_url="user_login")
def notification_app_index(request):
    context = dict()
    personne = None
    personnes = None
    personnes_select_box = None
    anniversaires = None

    jour_actuel = datetime.date.today().day
    mois_actuel = datetime.date.today().month
    annee_actuel = datetime.date.today().year

    pb = Pushbullet('o.fUXYFOfF5oufOF6AlwumRjxIQuvyyHno')
    all_anniv_actuel = Personne.objects.filter(date_naissance__day=jour_actuel, date_naissance__month=mois_actuel)
    if all_anniv_actuel:
        for elt in all_anniv_actuel:
            push = pb.push_note(
                f"Anniversaire de Vase d'honneur cameroun {annee_actuel} : ", 
                f"{elt.nom_et_prenom} Né le {elt.date_naissance.day} {month_name(elt.date_naissance.month)} {elt.date_naissance.year}"
            )

    if 'liste-anniv' in request.GET:
        try:
            #pers_select = Personne.objects.get(id=int(request.GET['liste-anniv']))
            anniversaires = Personne.objects.filter(date_naissance__month=int(request.GET['liste-anniv']))
            personnes = Personne.objects.filter(date_naissance__month=int(request.GET['liste-anniv']))
            context['mois_select'] = month_name(int(request.GET['liste-anniv']))
        except Personne.DoesNotExist:
            raise Http404("Pages non disponible")
        #context['pers_select'] = pers_select
    else:
        anniversaires = Personne.objects.filter(date_naissance__month=datetime.date.today().month)
        all_anniv_actuel = Personne.objects.filter(date_naissance__day=jour_actuel, date_naissance__month=mois_actuel)
        if all_anniv_actuel:
            context['is_you'] = True
        personnes = Personne.objects.all()
        try:
            send(request)
        except:
            print("==========/////*****------+++++++pas de connexion internet pour envoyer les notifications")

    context['anniversaires'] = anniversaires
    context['personnes'] = personnes
    context['personnes_select_box'] = Personne.objects.all()
    context['select_link'] = 'sms'
    return render(request, 'index.html', context)




def send_notification(registration_ids , message_title , message_desc):
    fcm_api = "AAAAJBdk1cg:APA91bGv8-77N2UDAoav7HksTFWNHCkNEFviAKq6e6FdGY9tfG0ZFYPAdnVXbgzhIdf3nw32C1oF3wFGmrD9l57YGDrk7fflXl0G3ODjYkhx619qZbc0puR3SprofgX2BtfJ6xh6SlJ6"
    url = "https://fcm.googleapis.com/fcm/send"
    
    headers = {
        "Content-Type":"application/json",
        "Authorization": 'key='+fcm_api
    }

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


@login_required(login_url="user_login")
def notification_app_recherche(request):
    context = dict()
    if 'liste-message' in request.GET:
        try:
            pers_select = Personne.objects.get(id=int(request.GET['liste-message']))
            personnes_send = Personne.objects.filter(date_naissance=pers_select.date_naissance)
        except Personne.DoesNotExist:
            raise Http404("Pages non disponible")

    context['pers_select'] = pers_select
    context['personnes_send'] = personnes_send
    return redirect('notification:notification_app_index')



@login_required(login_url="user_login")
def notification_app_ajouter_personne(request, type_opera):
    context = dict()
    form = None
    if request.method == 'POST':
        form = PersonneForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Personne ajouté avec success")
            return redirect('notification:notification_app_index')
    else:
        form = PersonneForm()
    context['form'] = form
    context['type_opera'] = type_opera
    context['personnes'] = Personne.objects.all()
    context['select_link'] = 'sms'
    return render(request, 'index.html', context)


@login_required(login_url="user_login")
def notification_app_detail_personne(request, type_opera, pk):
    context = dict()
    form = None
    personne = None
    try:
        personne = Personne.objects.get(id=pk)
        if request.method=="POST":
            form = PersonneForm(data=request.POST, instance=personne)
            if form.is_valid():
                form.save()
                messages.success(request, f"Personne modifier avec success")
                return redirect('notification:notification_app_index')
        else:
            form = PersonneForm(instance=personne)
            context['personne'] = personne
    except Personne.DoesNotExist:
        return Http404('page non disponible')

    context['pers_select'] = personne
    context['form'] = form
    context['type_opera'] = type_opera
    context['personnes'] = Personne.objects.all()
    context['select_link'] = 'sms'
    return render(request, 'index.html', context)


@login_required(login_url="user_login")
def notification_app_supprimer_personne(request, type_opera, pk):
    try:
        personne = Personne.objects.get(id=pk)
        personne.delete()
        messages.error(request, f"Supprission reuissie de {personne.nom_et_prenom}")
        return redirect('notification:notification_app_index')
    except Personne.DoesNotExist:
        return Http404('page non disponible')










