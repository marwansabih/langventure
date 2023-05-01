# Generated by Django 4.1.3 on 2023-05-01 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gapfiller', '0001_language_user_mother_language_user_target_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mother_language',
            field=models.TextField(blank=True, default='en'),
        ),
        migrations.AlterField(
            model_name='user',
            name='target_language',
            field=models.TextField(blank=True, default='de'),
        ),
    ]
