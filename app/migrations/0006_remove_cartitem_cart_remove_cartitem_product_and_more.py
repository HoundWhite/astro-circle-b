# Generated by Django 5.2.1 on 2025-06-18 06:24

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_service_options_cartitem_item_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='product',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='service',
        ),
        migrations.AlterModelOptions(
            name='service',
            options={},
        ),
        migrations.AlterField(
            model_name='service',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='service',
            name='image',
            field=models.ImageField(upload_to='services/'),
        ),
        migrations.AlterField(
            model_name='service',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status'),
        ),
        migrations.AlterField(
            model_name='user',
            name='telephon',
            field=models.CharField(max_length=20),
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='CartItem',
        ),
    ]
