# Generated by Django 3.1.3 on 2020-11-26 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djapp', '0007_auto_20201124_1821'),
    ]

    operations = [
        migrations.AddField(
            model_name='coach',
            name='blocked',
            field=models.DateTimeField(null=True),
        ),
    ]