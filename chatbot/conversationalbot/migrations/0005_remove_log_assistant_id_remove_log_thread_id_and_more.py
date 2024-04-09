# Generated by Django 4.0.8 on 2024-04-09 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversationalbot', '0004_usermeta_state'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='log',
            name='assistant_id',
        ),
        migrations.RemoveField(
            model_name='log',
            name='thread_id',
        ),
        migrations.AddField(
            model_name='usermeta',
            name='assistant_id',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='usermeta',
            name='thread_id',
            field=models.CharField(max_length=100, null=True),
        ),
    ]