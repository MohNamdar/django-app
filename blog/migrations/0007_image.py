# Generated by Django 5.0.4 on 2024-05-23 13:45

import django.db.models.deletion
import django_jalali.db.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_comment_created_alter_comment_updated_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_file', models.ImageField(upload_to='post-images/')),
                ('title', models.CharField(blank=True, max_length=250, null=True, verbose_name='موضوع')),
                ('description', models.TextField(blank=True, null=True)),
                ('created', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='blog.post', verbose_name='تصاویر')),
            ],
            options={
                'verbose_name': 'تصویر',
                'verbose_name_plural': 'تصاویر',
                'ordering': ['-created'],
                'indexes': [models.Index(fields=['-created'], name='blog_image_created_a116df_idx')],
            },
        ),
    ]
