# Generated by Django 5.0.7 on 2024-10-02 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='quatity',
            new_name='quantity',
        ),
        migrations.AlterField(
            model_name='orderplaced',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
