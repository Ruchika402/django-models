from django.contrib import admin

# Register your models here.
from .models import Book

admin.site.register(Book)
class BookAdmin(admin.ModelAdmin):
    
    #display list
    list_display = ['id','title','author','genre','published_date']
    
    # Fields to filter by
    list_filter = ['genre', 'published_date']
    
    # Search fields
    search_fields = ['title', 'author']
    
    # Ordering
    ordering = ['-published_date']
    
    # Fields to edit in list view
    list_editable = ['genre']
    
    # Pagination
    list_per_page = 20
    
    # Date hierarchy
    date_hierarchy = 'published_date'
    
    # Fields to show in detail form
    fields = ['title', 'author', 'genre', 'published_date']

    def rating_stars(self, obj):
        return '⭐' * obj.rating
    rating_stars.short_description = 'Rating Stars'