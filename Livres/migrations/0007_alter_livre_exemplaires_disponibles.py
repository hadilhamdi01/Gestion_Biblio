# Generated by Django 5.1.3 on 2024-12-27 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Livres', '0006_auteur_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='livre',
            name='exemplaires_disponibles',
            field=models.PositiveIntegerField(default=3),
        ),
    ]
