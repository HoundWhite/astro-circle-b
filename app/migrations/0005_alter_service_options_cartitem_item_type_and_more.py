# Generated by Django 5.2.1 on 2025-06-15 13:05

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_cart_cartitem'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='service',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddField(
            model_name='cartitem',
            name='item_type',
            field=models.CharField(choices=[('product', 'Товар'), ('service', 'Услуга')], default='product', max_length=10),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.service'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.product'),
        ),
        migrations.AlterField(
            model_name='service',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='image',
            field=models.ImageField(null=True, upload_to='services/'),
        ),
        migrations.AlterField(
            model_name='service',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='telephon',
            field=models.CharField(max_length=255),
        ),
    ]
