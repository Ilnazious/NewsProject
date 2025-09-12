from django.contrib import admin
from .models import Category, Post

def delcategory(modeladmin, request, queryset):
    deleted_count, _ = queryset.delete()
    modeladmin.message_user(request, f'Удалено категорий: {deleted_count}')
delcategory.short_description = '🗑️ Удалить категории'


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'dataCreation', 'categoryType')
    list_filter = ('title', 'dataCreation', 'categoryType')
    search_fields = ('title', 'title')
    actions = [delcategory]

admin.site.register(Category)
admin.site.register(Post, PostAdmin)