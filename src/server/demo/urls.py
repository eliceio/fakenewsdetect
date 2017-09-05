from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^feedback/$', views.feedback, name='feedback'),
    url(r'^ver2/$', views.ver2, name='ver2'),
    url(r'receiveData', views.receiveData, name='receiveData'),
    url(r'feedback_ver2', views.feedback_ver2, name='feedback_ver2'),
    url(r'resetCandidate', views.resetCandidate, name='resetCandidate'),
]
