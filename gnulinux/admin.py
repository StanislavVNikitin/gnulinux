from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe

from .models import *


# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    save_as = True
    save_on_top = True
    list_display = ("id", "user", "get_avatar")
    list_display_links = ("id", "user")
    search_fields = ("user",)
    readonly_fields = ("get_avatar",)
    fields = ("id", "user", "get_avatar", "birthday")

    def get_avatar(self, obj):
        if obj.avatar:
            return mark_safe(f'<img src="{obj.avatar.url}" width="50">')
        return "-"

    get_avatar.short_description = "Аватар"

class PageAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Page
        fields = "__all__"


class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    form = PageAdminForm
    save_as = True
    save_on_top = True
    list_display = ("id", "title", "slug", "created_at")
    list_display_links = ("id", "title")
    search_fields = ("title",)
    readonly_fields = ("created_at",)
    fields = ("title", "slug",  "content", "created_at")


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = "__all__"


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    form = PostAdminForm
    save_as = True
    save_on_top = True
    list_display = ("id", "title", "slug", "category", "created_at", "get_photo")
    list_display_links = ("id", "title")
    search_fields = ("title",)
    list_filter = ("category",)
    readonly_fields = ("views", "created_at", "get_photo")
    fields = ("title", "slug", "user", "category", "tags", "content", "photo", "get_photo", "views", "created_at")

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        return "-"

    get_photo.short_description = "Фото"


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    save_as = True
    save_on_top = True
    list_display = ("id", "title", "slug", "get_photo")
    list_display_links = ("id", "title")
    search_fields = ("title",)
    readonly_fields = ("get_photo",)
    fields = ("title", "slug", "photo", "get_photo")

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        return "-"

    get_photo.short_description = "Фото"


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    save_as = True
    save_on_top = True
    list_display = ("id", "title", "slug")
    list_display_links = ("id", "title")
    search_fields = ("title",)
    fields = ("title", "slug")


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)


admin.site.site_title = 'Управление сайтом GnuLinux'
admin.site.site_header = 'Управление сайтом GnuLinux'
