from django.contrib import admin
from .models import TravelOption

@admin.register(TravelOption)
class TravelOptionAdmin(admin.ModelAdmin):
    list_display = ('type', 'source', 'destination', 'date_time', 'price', 'available_seats')
    list_filter = ('type', 'source', 'destination', 'date_time')
    search_fields = ('source', 'destination', 'type')
    ordering = ('date_time',)
