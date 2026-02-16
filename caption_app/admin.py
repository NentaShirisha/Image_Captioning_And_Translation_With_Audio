from django.contrib import admin
from .models import CaptionHistory

@admin.register(CaptionHistory)
class CaptionHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'caption', 'language', 'created_at')
    list_filter = ('language', 'created_at')
    search_fields = ('caption', 'translated_text')