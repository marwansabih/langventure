# Generated by Django 4.1.3 on 2023-05-01 12:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gapfiller', '0002_alter_user_mother_language_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='mother_language',
        ),
        migrations.RemoveField(
            model_name='user',
            name='target_language',
        ),
    ]
