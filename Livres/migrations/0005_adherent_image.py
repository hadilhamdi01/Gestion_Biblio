# Generated by Django 5.1.3 on 2024-12-25 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Livres', '0004_livre_exemplaires_disponibles_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='adherent',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='adherents/'),
        ),
    ]