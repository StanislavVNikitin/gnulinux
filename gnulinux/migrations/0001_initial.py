# Generated by Django 4.2.6 on 2023-10-12 10:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Url категории')),
                ('photo', models.ImageField(blank=True, upload_to='photo/category/', verbose_name='Картинка')),
                ('class_name', models.CharField(max_length=100, verbose_name='Класс CSS')),
                ('deleted', models.BooleanField(default=False, verbose_name='Удалено')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название страницы')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Url страницы')),
                ('content', models.TextField(blank=True, verbose_name='Текст страницы')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликовано')),
                ('deleted', models.BooleanField(default=False, verbose_name='Удалено')),
            ],
            options={
                'verbose_name': 'Страница',
                'verbose_name_plural': 'Страницы',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='Url тэга')),
            ],
            options={
                'verbose_name': 'Тэг',
                'verbose_name_plural': 'Тэги',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(default='default.jpg', upload_to='profile_pics')),
                ('birthday', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название новости')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Url новости')),
                ('content', models.TextField(blank=True, verbose_name='Текст новости')),
                ('photo', models.ImageField(blank=True, upload_to='photo/%Y/%m/%d/', verbose_name='Картинка')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('views', models.IntegerField(default=0, verbose_name='Количество просмотров')),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликовано')),
                ('deleted', models.BooleanField(default=False, verbose_name='Удалено')),
                ('category', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='posts', to='gnulinux.category', verbose_name='Категория')),
                ('tags', models.ManyToManyField(blank=True, related_name='posts', to='gnulinux.tag', verbose_name='Тэг')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Новость',
                'verbose_name_plural': 'Новости',
                'ordering': ['-created_at'],
            },
        ),
    ]