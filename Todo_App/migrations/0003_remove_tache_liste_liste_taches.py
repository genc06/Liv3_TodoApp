# Generated by Django 5.0.2 on 2024-02-19 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Todo_App', '0002_remove_liste_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tache',
            name='liste',
        ),
        migrations.AddField(
            model_name='liste',
            name='taches',
            field=models.ManyToManyField(related_name='listes', to='Todo_App.tache'),
        ),
    ]