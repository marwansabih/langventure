# Generated by Django 4.1.3 on 2023-02-21 17:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0012_dialog_translation_option_translation_optiontokens_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Knowledge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='actor',
            name='left',
            field=models.TextField(default='50px'),
        ),
        migrations.AlterField(
            model_name='actor',
            name='top',
            field=models.TextField(default='100px'),
        ),
        migrations.AddField(
            model_name='optiontokens',
            name='aquired',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='aquire_options', to='story.knowledge'),
        ),
        migrations.AddField(
            model_name='optiontokens',
            name='disabled_k_items',
            field=models.ManyToManyField(related_name='disabled_options', to='story.knowledge'),
        ),
        migrations.AddField(
            model_name='optiontokens',
            name='required_k_items',
            field=models.ManyToManyField(related_name='require_options', to='story.knowledge'),
        ),
    ]
