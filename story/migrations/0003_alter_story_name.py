# Generated by Django 4.1.3 on 2023-01-16 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0002_story_finished_story_name_story_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='name',
            field=models.TextField(),
        ),
    ]
