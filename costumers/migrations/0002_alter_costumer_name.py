# Generated by Django 5.0.2 on 2024-03-05 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('costumers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='costumer',
            name='name',
            field=models.TextField(max_length=20),
        ),
    ]
