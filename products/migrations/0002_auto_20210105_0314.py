# Generated by Django 3.1.4 on 2021-01-04 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='views',
        ),
        migrations.AlterField(
            model_name='product',
            name='condition',
            field=models.CharField(choices=[('new', 'New'), ('used', 'Used')], max_length=10),
        ),
    ]