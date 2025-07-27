# Version corrigé sans input
import streamlit as st
import requests
import pandas as pd
from io import BytesIO

# 🔐 Ta clé API TMDb (à personnaliser)
API_KEY = '26e43b5e331dafd95b1459d14665eb66' #'ta_cle_api_tmdb'

# 📡 Fonction de recherche d'infos
def get_tv_series_info(title):
    search_url = 'https://api.themoviedb.org/3/search/tv'
    params = {'api_key': API_KEY, 'query': title, 'language': 'fr-FR'}
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
    details = requests.get(f'https://api.themoviedb.org/3/tv/{tv_id}', params={'api_key': API_KEY, 'language': 'fr-FR'}).json()
    credits = requests.get(f'https://api.themoviedb.org/3/tv/{tv_id}/credits', params={'api_key': API_KEY}).json()

    main_actor = credits.get('cast', [{}])[0].get('name', 'Inconnu')
    producers = [p['name'] for p in credits.get('crew', []) if 'Producer' in p.get('job', '')]
    producer = producers[0] if producers else 'Inconnu'

    return {
        'Titre': details.get('name', title),
        'Année de création': details.get('first_air_date', 'N/A')[:4],
        'Nombre de saisons': details.get('number_of_seasons', 'N/A'),
        'Producteur': producer,
        'Acteur principal': main_actor
    }

# 🎨 Interface utilisateur Streamlit
st.set_page_config(page_title="Recherche de séries", layout="centered")
st.title("📺 Recherche d'infos sur des séries TV")

user_input = st.text_area("Entrez les titres des séries, séparés par des virgules :", placeholder="Ex : Breaking Bad, Dark, The Office")

if st.button("🔍 Rechercher") and user_input:
    titres = [t.strip() for t in user_input.split(',') if t.strip()]
    resultats = [get_tv_series_info(t) for t in titres]

    df = pd.DataFrame(resultats)
    st.success("✅ Résultats trouvés")
    st.dataframe(df)

    output = BytesIO()
    df.to_excel(output, index=False, engine='openpyxl')
    output.seek(0)

    st.download_button(
        label="⬇️ Télécharger les résultats en Excel",
        data=output,
        file_name="infos_series.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

