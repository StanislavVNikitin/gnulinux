import datetime
from django.db import models

from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse

# Create your models here.
"""
Model Profile
"""
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.png', upload_to='profile_pics')
    birthday = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 120 or img.width > 120:
            output_size = (120, 120)
            img.thumbnail(output_size)
            img.save(self.avatar.path)

    def get_age(self):
        age = datetime.date.today() - self.birthday
        return int((age).days / 365.25)

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
        ordering = ["user"]


"""
Model Category
"""
class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255, verbose_name="Url категории", unique=True)
    photo = models.ImageField(upload_to="photo/category/", blank=True, verbose_name="Картинка")
    class_name = models.CharField(max_length=100, blank=True, verbose_name="Класс CSS")
    deleted = models.BooleanField(default=False, verbose_name='Удалено')

    def __str__(self):
        return self.title

    def delete(self, *args):
        self.deleted = True
        self.save()

    def get_absolute_url(self):
        return reverse("gnulinux:category", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["title"]


"""
Model Tag
"""
class Tag(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(max_length=100, verbose_name="Url тэга", unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("gnulinux:tag", kwargs={"slug": self.slug})

    def delete(self, *args):
        self.deleted = True
        self.save()

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"
        ordering = ["title"]


"""
Model Post
"""
class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название новости")
    slug = models.SlugField(max_length=255, verbose_name="Url новости", unique=True)
    content = models.TextField(blank=True, verbose_name="Текст новости")
    photo = models.ImageField(upload_to="photo/%Y/%m/%d/", blank=True, verbose_name="Картинка")
    category = models.ForeignKey("Category", blank=True, on_delete=models.PROTECT, related_name="posts",
                                 verbose_name="Категория")
    tags = models.ManyToManyField("Tag", blank=True, related_name="posts", verbose_name="Тэг")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts",
                             verbose_name="Пользователь")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    views = models.IntegerField(default=0, verbose_name="Количество просмотров")
    pin = models.BooleanField(default=False, verbose_name='Закрепить')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    deleted = models.BooleanField(default=False, verbose_name='Удалено')

    def __str__(self):
        return self.title

    def delete(self, *args):
        self.deleted = True
        self.save()

    def get_absolute_url(self):
        return reverse("gnulinux:post", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ["-created_at"]

"""
Model Page
"""
class Page(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название страницы")
    slug = models.SlugField(max_length=255, verbose_name="Url страницы", unique=True)
    content = models.TextField(blank=True, verbose_name="Текст страницы")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    deleted = models.BooleanField(default=False, verbose_name='Удалено')

    def __str__(self):
        return self.title

    def delete(self, *args):
        self.deleted = True
        self.save()

    def get_absolute_url(self):
        return reverse("gnulinux:page", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"
        ordering = ["-created_at"]
