import json
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# Remplace <db_password> par ton mot de passe MongoDB
uri = "mongodb+srv://guerahamel0:7GIv5VJLtEdoeOis@cluster0.0vwfe.mongodb.net/"

try:
    # Connexion à MongoDB
    client = MongoClient(uri)

    # Sélectionner la base de données et la collection
    db = client.scraping_job
    collection = db.cluster0

    # Charger les détails des offres
    with open("details_offres.json", "r", encoding="utf-8") as file:
        offres_details = json.load(file)
    # Insérer les données dans MongoDB
    collection.insert_many(offres_details)
    print(f"✅ {len(offres_details)} offres insérées dans MongoDB.")

    # Charger les détails des offres
    with open("IndeedScraper.json", "r", encoding="utf-8") as file:
        offres_details = json.load(file)
    # Insérer les données dans MongoDB
    collection.insert_many(offres_details)
    print(f"✅ {len(offres_details)} offres insérées dans MongoDB.")

except ConnectionFailure:
    print("⚠️ Échec de la connexion à MongoDB.")
except Exception as e:
    print(f"⚠️ Une erreur s'est produite : {e}")
finally:
    # Fermer la connexion
    client.close()
