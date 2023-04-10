from django.urls import path
from . import views

urlpatterns = [
    path('postPerson/', views.createPerson),
    #path('getPerson/<str:token>/', views.getPerson),
    path('postMessage/', views.postMessage),
    path('getMessages/<int:token>/', views.getMessages),
    path('postConversations/', views.getConversations)
]