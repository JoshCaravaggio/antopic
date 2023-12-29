import os
from rest_framework import generics
from .models import Topic
from .serializers import TopicSerializer
from functools import wraps
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, permissions, authentication
from .models import Topic, Content
from .serializers import TopicSerializer, ContentSerializer
import jwt
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .ingestion import ingest_content
from django.http import JsonResponse, HttpResponseNotFound
from django.http import Http404
from django.conf import settings
import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.chains import RetrievalQA
from langchain import OpenAI
import pinecone
from django.core.files.storage import default_storage
from rest_framework.parsers import MultiPartParser, JSONParser
from langchain.chat_models import ChatOpenAI


def get_token_auth_header(request):
    auth = request.META.get("HTTP_AUTHORIZATION", None)
    parts = auth.split()
    token = parts[1]

    return token


def requires_scope(required_scope):
    def require_scope(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = get_token_auth_header(args[0])
            decoded = jwt.decode(token, verify=False)
            if decoded.get("scope"):
                token_scopes = decoded["scope"].split()
                for token_scope in token_scopes:
                    if token_scope == required_scope:
                        return f(*args, **kwargs)
            response = JsonResponse(
                {'message': 'You don\'t have access to this resource'})
            response.status_code = 403
            return response
        return decorated
    return require_scope

def chat(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        print(data)
        question = data.get('question')
        history = data.get('history') or []
        topic_id = data.get('topicId')
        if not question:
            return JsonResponse({"message": "No question in the request"}, status=400)

        sanitized_question = question.strip().replace('\n', ' ')
        chain = get_chain(topic_id)
        try:
            answer = chain.run(query=sanitized_question,
                               history=history, max_docs=2, max_tokens=100)
            history.append(answer)
            return JsonResponse({"answer": answer, "history": history})
        except Exception as error:
            print('error', error)

        return JsonResponse({"message": "Error during interaction"}, status=500)
    else:
        return JsonResponse({"message": "Invalid request method"}, status=405)


def get_chain(topic_id):
    print("Initiating pinecone store", topic_id)
    pinecone.init(api_key=os.environ['PINECONE_API_KEY'],
                  environment=os.environ['PINECONE_ENV'])
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002",
                                  chunk_size=1000)
    vectorstore = Pinecone.from_existing_index(
        os.environ['PINECONE_INDEX'], embeddings, namespace=topic_id)
    chain = RetrievalQA.from_chain_type(llm=ChatOpenAI(openai_api_key=os.environ['OPENAI_API_KEY'], max_tokens=512, model_name="gpt-4"),
                                        chain_type="stuff",
                                        retriever=vectorstore.as_retriever())
    return chain


class TopicListCreate(generics.ListCreateAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.auth.payload.get('sub')
        return Topic.objects.filter(user_id=user_id)

    def perform_create(self, serializer):
        user_id = self.request.auth.payload.get('sub')
        serializer.save(user_id=user_id)


class TopicRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.auth.payload.get('sub')
        return Topic.objects.filter(user_id=user_id)


class ContentListCreate(generics.ListCreateAPIView):
    serializer_class = ContentSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, JSONParser]

    def get_queryset(self):
        user_id = self.request.auth.payload.get('sub')
        return Content.objects.filter(topic__user_id=user_id)

    def perform_create(self, serializer):

        user_id = self.request.auth.payload.get('sub')
        topic_id = self.request.data.get('topic', None)
        if not topic_id:
            raise ValidationError("A topic must be provided")

        matching_topics = Topic.objects.filter(user_id=user_id, _id=topic_id)
        topic = matching_topics.first()

        if not topic:
            raise ValidationError("No Topic matches the given query.")

        content_path = os.environ['CONTENT_PATH']
        serializer.save(topic=topic, state="processing")
        content_type = self.request.data.get('type', None)
        if content_type in ['mp3', 'pdf', 'txt']:
            if 'file' in self.request.FILES:
                file = self.request.FILES['file']
                content_id = serializer.data.get(("_id"))
                subfolder = f"{content_path}/{topic_id}/{content_id}"
                file_path = f"{subfolder}/{file.name}"
                default_storage.save(file_path, file)
            else:
                raise ValidationError(
                    "A file must be provided for mp3, pdf, or txt content types")

        try:
            # print("CAlling ingest content")
            print(settings.CELERY_BROKER_URL)
            ingestion_task = ingest_content.delay(serializer.data.get(("_id")))
            print("Task Added:", ingestion_task)

            # set the task_id on the topic
        except Exception as e:
            print("Ingestion enqueueing failed")
            print(e)


class ContentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ContentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.auth.payload.get('sub')
        return Content.objects.filter(topic__user_id=user_id)
