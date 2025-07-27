import requests
import pandas as pd

# Clé API TMDb (à remplacer par la tienne)
API_KEY = '26e43b5e331dafd95b1459d14665eb66' #'ta_cle_api_tmdb'

def get_tv_series_info(title):
    # Recherche de la série
    search_url = 'https://api.themoviedb.org/3/search/tv'
    params = {
        'api_key': API_KEY,
        'query': title,
        'language': 'fr-FR'
    }
    response = requests.get(search_url, params=params)
    results = response.json().get('results')

    if not results:
        return {
            'Titre': title,
            'Année de création': 'Non trouvée',
            'Nombre de saisons': 'Non trouvée',
            'Producteur': 'Non trouvé',
            'Acteur principal': 'Non trouvé'
        }

    tv_id = results[0]['id']

    # Détails
    details_url = f'https://api.themoviedb.org/3/tv/{tv_id}'
    details = requests.get(details_url, params={'api_key': API_KEY, 'language': 'fr-FR'}).json()

    # Crédits
    credits_url = f'https://api.themoviedb.org/3/tv/{tv_id}/credits'
    credits = requests.get(credits_url, params={'api_key': API_KEY}).json()

    # Acteur principal
    main_actor = credits.get('cast', [{}])[0].get('name', 'Inconnu')

    # Producteurs
    producers = [p['name'] for p in credits.get('crew', []) if 'Producer' in p.get('job', '')]
    producer = producers[0] if producers else 'Inconnu'

    return {
        'Titre': details.get('name', title),
        'Année de création': details.get('first_air_date', 'N/A')[:4],
        'Nombre de saisons': details.get('number_of_seasons', 'N/A'),
        'Producteur': producer,
        'Acteur principal': main_actor
    }

# ✅ Entrée utilisateur
user_input = input("Entrez les titres des séries, séparés par des virgules :\n")
titres = [titre.strip() for titre in user_input.split(',') if titre.strip()]

# ✅ Traitement de toutes les séries
resultats = []
for titre in titres:
    print(f"📺 Recherche en cours pour : {titre}")
    info = get_tv_series_info(titre)
    resultats.append(info)

# ✅ Affichage + Export
df = pd.DataFrame(resultats)
print("\n✅ Résultats récupérés :\n", df)

nom_fichier = "infos_series.xlsx"
df.to_excel(nom_fichier, index=False)
print(f"\n📁 Données exportées dans : {nom_fichier}")
