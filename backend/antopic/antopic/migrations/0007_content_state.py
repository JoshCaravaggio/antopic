# Generated by Django 4.1.8 on 2023-04-15 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('antopic', '0006_content_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='state',
            field=models.CharField(default='ingesting', max_length=255),
        ),
    ]
