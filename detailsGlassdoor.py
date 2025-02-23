import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def scrape_details_glassdoor(driver, link):
    """Scrape les détails d'une offre Glassdoor à partir de son lien."""
    driver.get(link)
    time.sleep(5)

    try:
        entreprise = driver.find_element(By.CSS_SELECTOR, "h4.heading_Subhead__Ip1aW").text
    except:
        entreprise = "Non précisé"

    try:
        titre = driver.find_element(By.CSS_SELECTOR, "h1.heading_Level1__soLZs").text
    except:
        titre = "Non précisé"

    try:
        localisation = driver.find_element(By.CSS_SELECTOR, "div[data-test='location']").text
    except:
        localisation = "Non précisé"

    try:
        description = driver.find_element(By.CSS_SELECTOR, "div.JobDetails_jobDescription__uW_fK").text
    except:
        description = "Non précisé"

    return {
        "title": titre,
        "entreprise": entreprise,
        "localisation": localisation,
        "contrat": "Non précisé",  # Glassdoor n'affiche pas forcément le type de contrat
        "description": description,
        "link": link
    }

# Charger les offres Glassdoor depuis le fichier JSON
with open("offres_glassdoor.json", "r", encoding="utf-8") as file:
    offres_glassdoor = json.load(file)

# Charger les détails existants pour éviter d'écraser les offres de HelloWork
try:
    with open("details_offres.json", "r", encoding="utf-8") as file:
        details_offres = json.load(file)
except FileNotFoundError:
    details_offres = []  # Si le fichier n'existe pas encore, initialiser une liste vide.

# Initialiser WebDriver
service = Service(executable_path="./chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Scraper les détails des offres Glassdoor
for offre in offres_glassdoor:
    print(f"🔍 Extraction des détails pour : {offre['Titre']}")
    details = scrape_details_glassdoor(driver, offre["Lien"])
    details_offres.append(details)

# Sauvegarder les offres HelloWork + Glassdoor dans le fichier JSON
with open("details_offres.json", "w", encoding="utf-8") as file:
    json.dump(details_offres, file, indent=4, ensure_ascii=False)

print(f"✅ {len(details_offres)} offres détaillées enregistrées dans details_offres.json")

driver.quit()
