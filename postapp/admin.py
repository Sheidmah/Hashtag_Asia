from django.contrib import admin
from postapp.models import Post, Genre, Year, State, Language, Country, Type, Days, Comment, Download, Frame, PIN_POST, \
    Askformovie

from django.contrib import admin



@admin.register(State,Year,Days,Language,Country,Type,Genre,Download,Frame)
class PersonAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published', 'active')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created', 'active')
    list_filter = ('active', 'created')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)

@admin.register(PIN_POST)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'active', 'published')

# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('email', 'name', 'post', 'active')
#     date_hierarchy = 'created'



@admin.register(Askformovie)
class AskformovieAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created', 'active')
    list_filter = ('active', 'created')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
