from django.contrib import admin
from django.contrib import admin
from .models import *
from django.contrib.admin.sites import AlreadyRegistered

# Register Category only if not already registered
try:
    admin.site.register(Category)
except AlreadyRegistered:
    pass

# Now define the admin class
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'description')

# Re-register with the custom admin class (remove the above try-except block if you use this)
try:
    admin.site.unregister(Category)  # Remove old registration if any
except admin.sites.NotRegistered:
    pass

admin.site.register(Category, CategoryAdmin)

# Register other models
admin.site.register(Products)
