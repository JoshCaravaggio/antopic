# Generated by Django 4.1.8 on 2023-04-16 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('antopic', '0007_content_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='task_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
