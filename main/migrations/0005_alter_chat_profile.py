# Generated by Django 5.1.2 on 2025-01-15 17:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_message_chat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.profile'),
        ),
    ]
