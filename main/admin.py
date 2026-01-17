from django.contrib import admin
from .models import *

admin.site.register(About)
admin.site.register(Service)
admin.site.register(Flight)
admin.site.register(ContactRequest)

class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [PhotoInline]

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('category', 'id')
