# Generated by Django 5.0.1 on 2024-03-17 18:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0008_thread'),
    ]

    operations = [
        migrations.RenameField(
            model_name='thread',
            old_name='thread',
            new_name='thread_id',
        ),
    ]
