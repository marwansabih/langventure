# Generated by Django 4.1.3 on 2022-12-11 13:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gapfiller', '0001_userentrychoiceselconfig_enabled'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserEntryGapFillerStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=False)),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entry_stati', to='gapfiller.entry')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entry_stati', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
