from django.urls import path
from . import views
from django.conf.urls import url
# from .views import RegisterView

urlpatterns = [
    path('', views.index, name='home'),
    path('key-exchange/', views.key_exchange, name='key-exchange'),
    path('accept-key-exchange/', views.accept_key_exchange, name='accept-key-exchange'),
    path('encryption-algorithms/', views.algoritms_cript, name='encryption-algorithms'),
    path('decryption-algorithms/', views.algoritms_decript, name='decryption-algorithms'),
    path('create-signature/', views.create_sig, name='create-signature'),
    path('check-signature/', views.checking_sig, name='check-signature'),
    path('create-author/', views.create_author, name='create-author'),
    path('check-author/', views.check_author, name='check-author'),
    # url(r'^registration-done/$', views.registration_done, name='registration-done'),
    url(r'^registration/$', views.Register_user, name='registration'),
    url(r'^login/$', views.log_in, name='login'),
    url(r'^logout/$', views.log_out, name='logout'),
]