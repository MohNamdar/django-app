# Generated by Django 5.0.3 on 2024-04-16 14:18

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_comment_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='انتشار'),
        ),
        migrations.AlterField(
            model_name='post',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
