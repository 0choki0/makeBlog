# Generated by Django 5.0.1 on 2024-02-05 15:15

import django_resized.forms
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=django_resized.forms.ResizedImageField(crop=['middle', 'center'], default='C:\\Users\\19wlg\\Desktop\\SIDE_PROJECT\\Blog\\staticfiles\\img/default.png', force_format=None, keep_meta=True, quality=-1, scale=None, size=[200, 200], upload_to='profile'),
        ),
    ]
