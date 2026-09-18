from django.contrib import admin
from .models import Genre, Story, Chapter, SavedStory, Comment


admin.site.register(Genre)
admin.site.register(Story)
admin.site.register(Chapter)
admin.site.register(SavedStory)
admin.site.register(Comment)