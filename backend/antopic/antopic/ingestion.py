import os
from celery import shared_task
from .video_embeddings import store_video_embeddings,  store_text_embeddings, store_audio_embeddings, store_pdf_embeddings
from antopic.serializers import ContentSerializer
import django
import nltk


@shared_task(bind=True)
def ingest_content(self, id):
    nltk.data.path.append('/app/nltk_data')
    from antopic.models import Content
    content = Content.objects.filter(_id=id).first()
    content.state = "processing"
    content.task_id = self.request.id
    content.save()
    content_base_path = os.environ['CONTENT_PATH']
    content_path = f'{content_base_path}/{content.topic._id}/{content._id}'
    print(content.url)
    try:
        if id:
            print("Processing content")
            if content:
                if content.type == 'youtube':
                    store_video_embeddings(
                        content.url, content._id, content.topic._id)
                elif content.type == 'txt':
                    store_text_embeddings(
                        f'{content_path}/{content.filename}', content._id, content.topic._id)
                elif content.type == 'pdf':
                    store_pdf_embeddings(
                        f'{content_path}/{content.filename}', content._id, content.topic._id)

                elif content.type == 'mp3':
                    store_audio_embeddings(
                        f'{content_path}/{content.filename}', content._id, content.topic._id)
                else:
                    raise Exception("Invalid content type")
                content.state = "processed"
                content.save()
        else:
            print("No messages in the queue.")
            
    except Exception as e:
        content.state = "failed"
        content.save()
        print("Error: ", e)
