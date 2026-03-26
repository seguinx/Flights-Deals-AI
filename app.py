from flask import Flask, render_template, request, url_for
import json
import os
from datetime import datetime
import requests
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# TA clé aviationstack (met-la dans .env)
API_KEY = os.getenv('API_KEY')

# 1. Créer le site Flask
app = Flask(__name__, static_folder='static', static_url_path='/static', template_folder='templates')

# 2. Fonction qui cherche les vols
def chercher_vols(depart, arrivee):
    url = "http://api.aviationstack.com/v1/flights"
    params = {
        'access_key': API_KEY,
        'dep_iata': depart,
        'arr_iata': arrivee,
        'limit': 10
    }

    r = requests.get(url, params=params)

    # Si l’API répond OK
    if r.status_code == 200:
        data = r.json()
        # Sauvegarde locale (optionnel)
        os.makedirs('data', exist_ok=True)
        nom_fichier = f"data/vols_{depart}_{arrivee}_{datetime.now().strftime('%H%M')}.json"
        with open(nom_fichier, 'w') as f:
            json.dump(data, f, indent=2)
        # On retourne la liste des vols
        return data.get('data', [])
    else:
        print(f"❌ Erreur API: {r.status_code}")
        return []

# 3. Page d’accueil (le formulaire)
@app.route('/')
def index():
    print("📁 Templates trouvés:", os.listdir('templates/'))
    return render_template('acceuil.html')

# 4. Route quand on clique sur "Rechercher"
@app.route('/chercher', methods=['POST'])
def chercher():
    # Prend ce que l’utilisateur a écrit dans le formulaire
    depart = request.form.get('depart')
    arrivee = request.form.get('arrivee')

    # Si manque départ ou arrivée
    if not depart or not arrivee:
        return "Veuillez entrer un départ et une arrivée", 400

    # Va chercher les vols avec ton API
    vols = chercher_vols(depart, arrivee)

    # Renvoie la même page HTML, mais avec les données
    return render_template('acceuil.html', depart=depart, arrivee=arrivee, vols=vols)

# 5. Lancer le site
if __name__ == "__main__":
    app.run(debug=True)
