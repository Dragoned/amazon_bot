# Generated by Django 3.2.9 on 2021-11-21 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AmazonBotSites', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prodotto',
            name='descrizione',
            field=models.TextField(blank=True, null=True),
        ),
    ]