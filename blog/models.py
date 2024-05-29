from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django_jalali.db import models as jmodels
from django.urls import reverse
from datetime import datetime
from django.template.defaultfilters import slugify


# custom manager
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)


# Create your models here.
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DR', 'منتشر نشده'
        PUBLISHED = 'PD', 'منتشر شده'
        REJECTED = 'RJ', 'رد شده'

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_post', verbose_name='نویسنده')
    title = models.CharField(max_length=250, verbose_name='موضوع')
    description = models.TextField()
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT, verbose_name='وضعیت')
    slug = models.SlugField(max_length=250)

    publish = jmodels.jDateTimeField(default=timezone.now, verbose_name='انتشار')
    created = jmodels.jDateTimeField(auto_now_add=True)
    updated = jmodels.jDateTimeField(auto_now=True)

    reading_time = models.PositiveIntegerField(verbose_name='زمان مطالعه')

    # objects = models.Manager()
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.reading_time:
            des_word = len(self.description.split())
            self.reading_time = (des_word // 230) or 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_details', args=[self.id])


class Ticket(models.Model):
    name = models.CharField(max_length=250, verbose_name='نام')
    subject = models.CharField(max_length=250, verbose_name='موضوع')
    message = models.TextField(verbose_name='متن پیام')
    phone = models.CharField(max_length=11, verbose_name='شماره تلفن')
    email = models.EmailField(verbose_name='ایمیل')

    class Meta:
        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت ها'

    def __str__(self):
        return self.name


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments", verbose_name='پست')
    name = models.CharField(max_length=250, verbose_name='نام')
    body = models.TextField(verbose_name='متن کامنت')
    email = models.EmailField(verbose_name='ایمیل', default='mail@email.com')
    created = jmodels.jDateTimeField(auto_now_add=True)
    updated = jmodels.jDateTimeField(auto_now=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'

    objects = models.Manager()
    actived = ActiveManager()

    def __str__(self):
        return f"{self.name} #{self.post}"


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images', verbose_name='پست')
    image_file = models.ImageField(upload_to=f"{datetime.now().year}/{datetime.now().month}")
    title = models.CharField(max_length=250, verbose_name='عنوان', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = jmodels.jDateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

        verbose_name = 'تصویر'
        verbose_name_plural = 'تصاویر'

    def __str__(self):
        return self.title if self.title else self.image_file.name.split('/')[-1]
