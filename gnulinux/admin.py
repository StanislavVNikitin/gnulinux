from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from .models import *


# Register your models here.
class DeleteUndeleteMixin:

    def mark_deleted(self, request, queryset):
        count = queryset.update(deleted=True)
        message = _(f"Удален, {count}")
        messages.add_message(request, messages.INFO, message)

    def un_delete(self, request, queryset):
        count = queryset.update(deleted=False)
        message = _(f"Снят с удаления, {count}")
        messages.add_message(request, messages.INFO, message)

    mark_deleted.short_description = _("Отметить на удалени")
    un_delete.short_description = _("Убрать отметку удаления")

class ProfileAdmin(admin.ModelAdmin):
    save_as = True
    save_on_top = True
    list_display = ("user", "get_avatar")
    list_display_links = ("user",)
    search_fields = ("user",)
    readonly_fields = ("get_avatar",)
    fields = ("user", "avatar", "get_avatar", "birthday")

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


class PostAdmin(admin.ModelAdmin, DeleteUndeleteMixin):
    prepopulated_fields = {"slug": ("title",)}
    form = PostAdminForm
    save_as = True
    save_on_top = True
    list_display = ("id", "title", "slug", "category", "is_published", "pin" , "created_at", "get_photo" , "deleted")
    list_display_links = ("id", "title")
    search_fields = ("title",)
    list_filter = ("category", "tags")
    readonly_fields = ("views", "created_at", "get_photo")
    fields = ("title", "slug", "user", "category", "tags", "content", "photo", "get_photo", "views", "created_at","is_published", "pin", "deleted")

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        return "-"

    get_photo.short_description = "Фото"


class CategoryAdmin(admin.ModelAdmin, DeleteUndeleteMixin):
    prepopulated_fields = {"slug": ("title",)}
    save_as = True
    save_on_top = True
    list_display = ("id", "title", "slug", "get_photo", "class_name", "deleted")
    list_display_links = ("id", "title")
    search_fields = ("title",)
    readonly_fields = ("get_photo",)
    fields = ("title", "slug", "class_name", "photo", "get_photo", "deleted")

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
