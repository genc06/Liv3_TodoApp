// Fonction pour supprimer une tâche
function supprimerTache(tacheId) {
    if (confirm("Êtes-vous sûr de vouloir supprimer cette tâche ?")) {
        fetch(`/supprimer_tache/${tacheId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}',
                'Content-Type': 'application/json'
            }
        }).then(response => {
            if (response.ok) {
                document.getElementById('tache-' + tacheId).remove(); // Supprimer la tâche de l'interface utilisateur
            }
        });
    }
}
function ajouterListe() {
    // Récupérer la valeur saisie par l'utilisateur
    var nouvelleListe = document.getElementById('nom-liste').value;

    // Effectuer une requête fetch pour ajouter la liste
    fetch('/ajouter_liste/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}', // Assurez-vous de remplacer csrf_token par la valeur réelle
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            nom_liste: nouvelleListe // Envoyer le nom de la nouvelle liste dans le corps de la requête
        })
    })
    .then(response => response.json())
    .then(data => {
        // Afficher le message de succès dans une boîte de dialogue pop-up
        alert(data.message);
        // Recharger la page ou faire d'autres actions si nécessaire
        location.reload();
    })
    .catch(error => {
        console.error('Erreur lors de l\'ajout de la liste :', error);
        // Gérer les erreurs si nécessaire
    });
}
// Fonction pour modifier une tâche
function modifierTache(tacheId) {
    const nouveauNomTache = prompt("Modifier la tâche :\n\nEntrez le nouveau nom de la tâche :");
    if (nouveauNomTache !== null && nouveauNomTache.trim() !== "") {
        const formData = new FormData();
        formData.append('nom', nouveauNomTache);
        fetch(`/modifier_tache/${tacheId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}'
            },
            body: formData
        }).then(response => {
            if (response.ok) {
                document.getElementById('tache-' + tacheId).getElementsByTagName('span')[0].innerText = nouveauNomTache;
                alert("La tâche a été modifiée avec succès !");
            } else {
                alert("Une erreur s'est produite lors de la modification de la tâche.");
            }
        }).catch(error => {
            console.error('Erreur lors de la modification de la tâche:', error);
            alert("Une erreur s'est produite lors de la modification de la tâche.");
        });
    }
}
function ajouterTache() {
    var nomTache = prompt('Entrez le nom de la tâche');
    if (nomTache) {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/ajouter-tache/', true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}');
        xhr.send('nom=' + encodeURIComponent(nomTache));
        xhr.onreadystatechange = function() {
            if (xhr.readyState !== 4) {
                return;
            }
            if (xhr.status !== 200) {
                return;
            }
            var tache = JSON.parse(xhr.responseText);
            var li = document.createElement('li');
            li.id = 'tache-' + tache.id;
            li.className = 'todo-item';
            var label = document.createElement('label');
            var input = document.createElement('input');
            input.type = 'checkbox';
            input.addEventListener('change', function () {
                var xhr = new XMLHttpRequest();
                xhr.open('POST', '/modifier-tache/' + tache.id + '/', true);
                xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}');
                xhr.send('completed=' + (input.checked ? 'true' : 'false'));
            });
            if (tache.completed) {
                input.checked = true;
            }
            label.appendChild(input);
            var span = document.createElement('span');
            span.textContent = tache.nom;
            label.appendChild(span);
            li.appendChild(label);
            var button = document.createElement('button');
            button.textContent = 'Supprimer';
            button.addEventListener('click', function () {
                var xhr = new XMLHttpRequest();
                xhr.open('POST', '/supprimer-tache/' + tache.id + '/', true);
                xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}');
                xhr.send();
                li.remove();
            });
            li.appendChild(button);
            button = document.createElement('button');
            button.textContent = 'Modifier';
            button.addEventListener('click', function () {
                var nouveauNom = prompt('Entrez le nouveau nom de la tâche', tache.nom);
                if (nouveauNom) {
                    var xhr = new XMLHttpRequest();
                    xhr.open('POST', '/modifier-tache/' + tache.id + '/', true);
                    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                    xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}');
                    xhr.send('nom=' + encodeURIComponent(nouveauNom));
                    xhr.onreadystatechange = function () {
                        if (xhr.readyState === 4 && xhr.status === 200) {
                            span.textContent = nouveauNom;
                        }
                    };
                }
            });
            li.appendChild(button);
            document.getElementById('todo-list').appendChild(li);
        };
    }
}
// Actualiser la page après avoir ajouté une liste
document.getElementById('add-list-form').addEventListener('submit', function(event) {
    event.preventDefault();
    // Recharger la page pour afficher le nouveau titre de la liste
    location.reload();
});
