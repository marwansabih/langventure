# Generated by Django 4.1.3 on 2023-03-14 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0018_alter_actor_top_alter_knowledge_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='knowledge',
            name='deactivated_scenes',
            field=models.ManyToManyField(blank=True, related_name='deactivates', to='story.scene'),
        ),
        migrations.AddField(
            model_name='knowledge',
            name='required_scenes',
            field=models.ManyToManyField(blank=True, related_name='requires', to='story.scene'),
        ),
    ]
