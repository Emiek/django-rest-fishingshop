# Generated by Django 4.2.7 on 2024-01-06 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='date_add',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='product',
            name='sold_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='total_rating',
            field=models.FloatField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='amount_rating',
            field=models.PositiveIntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='img_url',
            field=models.URLField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='rating',
            field=models.FloatField(default=None, null=True),
        ),
    ]