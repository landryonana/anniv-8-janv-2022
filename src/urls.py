from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


from evangelisation import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("accounts.urls")),
    path('', 
        views.notification_app_index, 
        name="notification_app_index"
    ),
    path('anniversaire/', include("evangelisation.urls")),
    
    path('send/' , views.send),
    path('firebase-messaging-sw.js',views.showFirebaseJS,name="show_firebase_js"),
]

urlpatterns += static(settings.STATIC_URL,   document_root=settings.STATIC_ROOT)
#urlpatterns += static(settings.MEDIA_URL,   document_root=settings.MEDIA_ROOT)
