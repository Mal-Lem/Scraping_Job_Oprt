import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_details_hellowork(driver, link):
    """Scrape les détails d'une offre HelloWork à partir de son lien."""
    driver.get(link)
    time.sleep(5)

    try:
        title = driver.find_element(By.CSS_SELECTOR, 'span[data-cy="jobTitle"]').text
    except:
        title = "Non précisé"

    try:
        entreprise = driver.find_element(By.CSS_SELECTOR, 'span.tw-contents.tw-typo-m.tw-text-grey').text
    except:
        entreprise = "Non précisé"

    try:
        # Localisation et Type de contrat sont dans le même style de balise,
        # mais séparés par une div de séparation.
        elements = driver.find_elements(By.CSS_SELECTOR, 'span.tw-inline-flex.tw-typo-m.tw-text-grey')
        localisation = elements[0].text if len(elements) > 0 else "Non précisé"
        contrat = elements[1].text if len(elements) > 1 else "Non précisé"
    except:
        localisation = "Non précisé"
        contrat = "Non précisé"

    try:
        description = driver.find_element(By.CSS_SELECTOR, 'p.tw-typo-long-m.tw-break-words').text
    except:
        description = "Non précisé"

    return {
        "title": title,
        "entreprise": entreprise,
        "localisation": localisation,
        "contrat": contrat,
        "description": description,
        "link": link
    }

# Charger les offres depuis offres_hellowork.json
with open("offres_hellowork.json", "r", encoding="utf-8") as file:
    offres = json.load(file)

# Initialiser WebDriver
service = Service(executable_path="./chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Scraper les détails des offres HelloWork
details_offres = []
for offre in offres:
    print(f"🔍 Extraction des détails pour : {offre['Titre']}")
    details = scrape_details_hellowork(driver, offre["Lien"])
    details_offres.append(details)

# Sauvegarde des détails dans un fichier JSON
with open("details_offres.json", "w", encoding="utf-8") as file:
    json.dump(details_offres, file, indent=4, ensure_ascii=False)

print(f"✅ {len(details_offres)} offres détaillées enregistrées dans details_offres.json")

driver.quit()
