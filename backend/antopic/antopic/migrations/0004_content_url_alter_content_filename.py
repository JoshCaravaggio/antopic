# Generated by Django 4.1.8 on 2023-04-13 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('antopic', '0003_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='content',
            name='filename',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
