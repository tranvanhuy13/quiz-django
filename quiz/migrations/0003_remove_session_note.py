# Generated by Django 5.2.4 on 2025-07-14 04:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_session_note'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='note',
        ),
    ]
