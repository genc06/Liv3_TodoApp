from django import forms
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.db import migrations, models

def set_default_value(apps, schema_editor):
    MyModel = apps.get_model('myapp', 'MyModel')
    MyModel.objects.update(new_field='default value')

class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mymodel',
            name='new_field',
            field=models.CharField(default='default value', max_length=255),
            preserve_default=False,
        ),
        migrations.RunPython(set_default_value),
    ]

class TacheListView(View):
    def get(self, request, liste_id):
        liste = get_object_or_404(Liste, pk=liste_id)
        taches = liste.taches.all()
        return render(request, 'index.html', {'liste': liste, 'taches': taches})
class Liste(models.Model):
    nom = models.CharField(max_length=255)

    def __str__(self):
        return self.nom


class Tache(models.Model):
    nom = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    liste = models.ForeignKey(Liste, on_delete=models.CASCADE, related_name='taches')

    def __str__(self):
        return self.nom


class TacheForm(forms.ModelForm):
    class Meta:
        model = Tache
        fields = ['nom']

    def clean_nom(self):
        nom = self.cleaned_data['nom']
        if len(nom) < 3:
            raise forms.ValidationError("Le nom de la tâche doit contenir au moins 3 caractères.")
        return nom


class ListeForm(forms.ModelForm):
    class Meta:
        model = Liste
        fields = ['nom']
