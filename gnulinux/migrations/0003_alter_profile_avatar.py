# Generated by Django 4.2.6 on 2023-10-12 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gnulinux', '0002_alter_profile_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='default.png', upload_to='profile_pics'),
        ),
    ]