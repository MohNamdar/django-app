from django.contrib import admin
from .models import *
from django_jalali.admin.filters import JDateFieldListFilter


# Inlines
class ImageInline(admin.TabularInline):
    model = Image
    extra = 0
    # fields = ['title']


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ['name', 'body']


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publish', 'status', 'reading_time']
    list_editable = ['status']
    list_filter = ['author', 'status', ('publish', JDateFieldListFilter), 'reading_time']
    search_fields = ['title', 'description']
    prepopulated_fields = {"slug": ['title']}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    inlines = [ImageInline, CommentInline]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'phone']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'post', 'created', 'active']
    list_editable = ['active']
    list_filter = ['name', 'post', ('created', JDateFieldListFilter)]
    search_fields = ['post', 'body']
    raw_id_fields = ['post']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['post', 'title']
