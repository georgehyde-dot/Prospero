# Generated by Django 5.0.1 on 2024-03-17 17:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0007_alter_nounchunk_version'),
    ]

    operations = [
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_posted', models.DateField()),
                ('thread', models.IntegerField()),
                ('article', models.CharField(max_length=256)),
                ('body', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.user')),
            ],
        ),
    ]
