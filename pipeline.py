import subprocess

print("🚀 Début du scraping et de l'insertion MongoDB...")

# Étape 1 : Scraper les offres
result_scraping = subprocess.run(["python", "main.py"])
if result_scraping.returncode == 0:
    print("✅ Extraction des offres réussie.")
    
    # Étape 2 : Scraper les détails HelloWork et Glassdoor
    result_details_hellowork = subprocess.run(["python", "detailsHellowork.py"])
    result_details_glassdoor = subprocess.run(["python", "detailsGlassdoor.py"])

    # Vérifier si les deux étapes ont réussi
    if result_details_hellowork.returncode == 0 and result_details_glassdoor.returncode == 0:
        print("✅ Détails HelloWork et Glassdoor extraits avec succès.")
        
        # Étape 3 : Insérer les données en base MongoDB
        result_insertion = subprocess.run(["python", "insertDB.py"])
        if result_insertion.returncode == 0:
            print("✅ Pipeline terminée!!")
        else:
            print("⚠️ Il y a un problème dans l'insertion des données en base MongoDB.")
    else:
        print("⚠️ Il y a un problème dans l'extraction des détails HelloWork ou Glassdoor.")
else:
    print("⚠️ Il y a un problème dans l'extraction des offres.")
