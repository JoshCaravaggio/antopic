from django.urls import path, include, register_converter
from .views import TopicListCreate, TopicRetrieveUpdateDestroy, ContentListCreate, ContentRetrieveUpdateDestroy, chat
from .converters import ObjectIDConverter

register_converter(ObjectIDConverter, 'objectid')

urlpatterns = [    
    path('chat',chat, name='chat' ),
    path('topics', TopicListCreate.as_view(), name='topics-list-create'),
    path('topics/<objectid:pk>', TopicRetrieveUpdateDestroy.as_view(), name='topic-retrieve-update-destroy'),
    path('contents', ContentListCreate.as_view(), name='content-list-create'),
    path('contents/<objectid:pk>', ContentRetrieveUpdateDestroy.as_view(), name='content-retrieve-update-destroy'),
]
