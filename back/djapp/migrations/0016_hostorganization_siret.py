# Generated by Django 3.1.5 on 2021-01-08 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djapp', '0015_auto_20201211_0951'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostorganization',
            name='siret',
            field=models.CharField(max_length=14, null=True),
        ),
    ]
