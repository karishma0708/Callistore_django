from django.urls import path
from calli_app import views
from calli import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('home',views.home),
    path('about',views.about),
    path('workshop',views.workshop),
    path('register',views.register),
    path('login',views.user_login),
    path('logout',views.user_logout),
    path('gifts',views.gifts),
    path('ser',views.ser),
    path('form_cont',views.form_cont),
    path('catfilter/<cv>',views.catfilter),
    path('addtocart/<pid>',views.addtocart),
    path('viewcart',views.viewcart),
    path('remove/<cid>',views.remove),
    path('updateqty/<qv>/<cid>',views.updateqty),
    path('placeorder',views.placeorder),
    path('makepayment',views.makepayment),
    path('sendmail/<uname>',views.sendusermail)

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
 