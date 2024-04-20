# Generated by Django 5.0.3 on 2024-04-15 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_post_options_post_reading_time_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created'], 'verbose_name': 'کامنت', 'verbose_name_plural': 'کامنت ها'},
        ),
        migrations.RemoveIndex(
            model_name='comment',
            name='blog_commen_created_0e6ed4_idx',
        ),
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['-created'], name='blog_commen_created_79f39f_idx'),
        ),
    ]
