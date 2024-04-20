# Generated by Django 5.0.3 on 2024-03-30 04:36

import django.db.models.deletion
import django.utils.timezone
import django_jalali.db.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='نام')),
                ('subject', models.CharField(max_length=250, verbose_name='موضوع')),
                ('message', models.TextField(verbose_name='متن پیام')),
                ('phone', models.CharField(max_length=11, verbose_name='شماره تلفن')),
                ('email', models.EmailField(max_length=254, verbose_name='ایمیل')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='موضوع')),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('DR', 'منتشر نشده'), ('PD', 'منتشر شده'), ('RJ', 'رد شده')], default='DR', max_length=2, verbose_name='وضعیت')),
                ('slug', models.SlugField(max_length=250)),
                ('publish', django_jalali.db.models.jDateTimeField(default=django.utils.timezone.now, verbose_name='انتشار')),
                ('created', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('updated', django_jalali.db.models.jDateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_post', to=settings.AUTH_USER_MODEL, verbose_name='نویسنده')),
            ],
            options={
                'ordering': ['-publish'],
                'indexes': [models.Index(fields=['-publish'], name='blog_post_publish_bb7600_idx')],
            },
        ),
    ]
