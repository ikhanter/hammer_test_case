# Generated by Django 5.0.4 on 2024-04-22 20:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('referral', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='password',
        ),
    ]
