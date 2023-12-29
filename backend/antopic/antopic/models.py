from djongo import models
from bson import ObjectId

class Topic(models.Model):
    _id = models.CharField(primary_key=True, editable=False, max_length=24)
    user_id = models.CharField(max_length=255)  
    task_id = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255)  
    title = models.CharField(max_length=255)
    description = models.TextField( blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self._id:
            self._id = str(ObjectId())
        self.state = 'created'
        super(Topic, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class Content(models.Model):
    _id = models.CharField(primary_key=True, editable=False, max_length=24)
    filename = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=100)
    title = models.CharField(max_length=255, blank=True, null=True)
    topic = models.ForeignKey(Topic, related_name='contents', on_delete=models.CASCADE)
    url = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, default='processing')  

    def __str__(self):
        return self.filename

    def save(self, *args, **kwargs):
        if not self._id:
            self._id = str(ObjectId())
        super(Content, self).save(*args, **kwargs)
