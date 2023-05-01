# Generated by Django 4.1.3 on 2023-05-01 12:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gapfiller', '0003_remove_user_mother_language_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='dest_language',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mother_language', to='gapfiller.language'),
        ),
        migrations.AddField(
            model_name='user',
            name='org_language',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='target_language', to='gapfiller.language'),
        ),
    ]
