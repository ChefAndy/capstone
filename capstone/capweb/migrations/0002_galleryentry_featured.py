# Generated by Django 2.2.11 on 2020-03-30 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capweb', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='galleryentry',
            name='featured',
            field=models.BooleanField(default=True, null=False),
        ),
    ]
