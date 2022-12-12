from django.db import migrations, models
from create_choices import create_undefinite_article_choices, create_definite_article_choices, create_conjunction_choices

class Migration(migrations.Migration):
    dependencies = [
        ('gapfiller', '0005_rule_name'),
    ]
    operations = [
        migrations.RunPython(create_undefinite_article_choices),
        migrations.RunPython(create_definite_article_choices),
        migrations.RunPython(create_conjunction_choices)
    ]
