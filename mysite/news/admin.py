from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms

from .models import News, Category

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'


class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    list_display = ('id', 'title', 'category', 'created_at', 'updated_at', 'is_published', 'get_photo')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published', 'category')
    list_filter = ('is_published', 'category')
    # поля, которые будут показаны при просмотре детально каждой новости ->
    # 'id', 'created_at', 'updated_at', 'get_photo', 'views' - не изменяемые поэтому не могут там оказаться
    fields = ('title', 'category', 'content', 'photo', 'is_published')
    # поля, которые нельзя изменить должны быть указаны в отдельном свойстве:
    readonly_fields = ('created_at', 'updated_at')  # FIX FIX FIX FIX FIX FIX FIX
    save_on_top = True

    def get_photo(self, obj):
        # возвращает промаркированный безопасным для тегов html
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width=50>')

    # чтобы в админке поменять get_photo на другую надпись
    get_photo.short_description = 'фото'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)


# в скобках важен порядок!
admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.site_title = 'Админка'
admin.site.site_header = 'Админка'


