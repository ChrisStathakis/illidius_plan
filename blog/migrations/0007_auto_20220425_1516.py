# Generated by Django 3.2.12 on 2022-04-25 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20180524_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postcategory',
            name='level',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='postcategory',
            name='lft',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='postcategory',
            name='rght',
            field=models.PositiveIntegerField(editable=False),
        ),
    ]