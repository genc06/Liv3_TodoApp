from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from django.core.paginator import Paginator
from django.http import HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.http import require_POST

from Todo_App.models import Tache, Liste, TacheForm, ListeForm


def showIndex(request):
    listes = Liste.objects.all()
    form_liste = ListeForm()
    form_tache = TacheForm()
    context = {
        'listes': listes,
        'form_liste': form_liste,
        'form_tache': form_tache,
    }
    return render(request, 'index.html', context)


def ajouter_tache(request):
    if request.method == 'POST':
        form = TacheForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('index')
            except IntegrityError as e:
                error_message = "Une erreur s'est produite lors de l'ajout de la tâche."
                return render(request, 'error.html', {'error_message': error_message})
    else:
        form = TacheForm()
    return render(request, 'index.html', {'form': form})


def modifier_tache(request, tache_id):
    tache = Tache.objects.get(pk=tache_id)
    if request.method == 'POST':
        form = TacheForm(request.POST, instance=tache)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = TacheForm(instance=tache)
    return render(request, 'index.html', {'form': form})


@require_POST
def modifier_liste(request, liste_id):
    nouveau_nom = request.POST.get('nouveau_nom')
    if nouveau_nom:
        liste = get_object_or_404(Liste, pk=liste_id)
        liste.nom = nouveau_nom
        liste.save()
        return redirect('index')
    else:
        return JsonResponse({'success': False, 'message': 'Le nouveau nom est requis.'})


def ajouter_liste(request):
    if request.method == 'POST':
        form = ListeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ListeForm()
    return render(request, 'index.html', {'form': form})


@csrf_exempt
def ajouter_tache_liste(request):
    if request.method == 'POST':
        form = TacheForm(request.POST)
        if form.is_valid():
            tache = form.save(commit=False)
            liste_id = request.POST.get('liste_id')
            if liste_id:
                # Use cache to store the Liste objects
                cache_key = f'liste_{liste_id}'
                liste = cache.get(cache_key)
                if not liste:
                    try:
                        liste = Liste.objects.select_related('tache').get(pk=liste_id)
                        cache.set(cache_key, liste)
                    except Liste.DoesNotExist:
                        return HttpResponseNotFound("La liste spécifiée n'existe pas.")
                tache.liste = liste
                tache.save()
                return redirect('index')
            else:
                return HttpResponseBadRequest("Veuillez fournir l'identifiant de la liste.")
        else:
            return HttpResponseBadRequest(form.errors)
    else:
        # Implement pagination for GET requests
        liste_list = Liste.objects.all()
        paginator = Paginator(liste_list, 10)  # Show 10 listes per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'index.html', {'page_obj': page_obj})


@csrf_exempt
def ajouter_tache_ajax(request):
    if request.method == 'POST':
        tache_nom = request.POST.get('nom')
        if tache_nom:
            try:
                tache = Tache.objects.create(nom=tache_nom)
                return JsonResponse({'success': True, 'message': 'La tâche a été ajoutée avec succès !', 'tache': {'id': tache.id, 'nom': tache.nom}})
            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)})
        else:
            return JsonResponse({'success': False, 'message': 'Le nom de la tâche est requis !'})
    else:
        return JsonResponse({'success': False, 'message': 'Méthode non autorisée !'})


def supprimer_tache(request, tache_id):
    if request.method == 'POST':
        tache = Tache.objects.get(pk=tache_id)
        tache.delete()
        return JsonResponse({'success': True, 'message': 'La tâche a été supprimée avec succès !'})
    else:
        return JsonResponse({'success': False, 'message': 'Méthode non autorisée !'})


def supprimer_liste(request, liste_id):
    if request.method == 'POST':
        try:
            liste = get_object_or_404(Liste, pk=liste_id)
            liste.delete()
            return JsonResponse({'success': True, 'message': 'La liste a été supprimée avec succès !'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Méthode non autorisée !'})
