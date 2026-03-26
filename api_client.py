import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')

def chercher_vols(depart, arrivee):
    url = f"http://api.aviationstack.com/v1/flights"
    params = {'access_key': API_KEY, 'dep_iata': depart, 'arr_iata': arrivee, 'limit': 10}
    
    r = requests.get(url, params=params)
    if r.status_code == 200:
        data = r.json()
        os.makedirs('data', exist_ok=True)
        nom_fichier = f"data/vols_{depart}_{arrivee}_{datetime.now().strftime('%H%M')}.json"
        
        with open(nom_fichier, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ {len(data['data'])} vols sauvés: {nom_fichier}")
    else:
        print(f"❌ Erreur {r.status_code}")

if __name__ == "__main__":
    print("🚀 Flights Deals AI")
    chercher_vols("YUL", "YYZ")
    chercher_vols("YUL", "BOS")
