# Generated by Django 5.0.3 on 2024-04-24 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_account_friends_message_chat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='messages',
            field=models.ManyToManyField(to='project.message'),
        ),
    ]