# Generated by Django 2.2.4 on 2021-09-29 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DstagramApp', '0006_auto_20210212_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='commentText',
            field=models.TextField(),
        ),
    ]