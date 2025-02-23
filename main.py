import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Importer les modules de scraping
from scraping.glassdoor import scrape_GlassDoor
from scraping.helloWork import scrape_hellowork

# Initialiser WebDriver
service = Service(executable_path="./chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Noms des fichiers JSON
json_filename_hellowork = "offres_hellowork.json"
json_filename_glassdoor = "offres_glassdoor.json"

try:
    driver.get("https://google.com/")

    # Attendre la barre de recherche
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "gLFyf")))

    # Entrer la requête de recherche
    input_element = driver.find_element(By.CLASS_NAME, "gLFyf")
    input_element.clear()
    time.sleep(2)
    input_element.send_keys("data engineer emploi paris" + Keys.ENTER)

    # Attendre et récupérer les liens des résultats
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[jsname='UWckNb']")))
    links = driver.find_elements(By.CSS_SELECTOR, "a[jsname='UWckNb']")

    job_sites = []
    for link in links[2:4]:  # On prend les 3e et 4e résultats
        url = link.get_attribute("href")
        title = link.find_element(By.TAG_NAME, "h3").text if link.find_elements(By.TAG_NAME, "h3") else "Sans titre"
        print(f"{title}: {url}")
        job_sites.append(url)

    # Listes pour stocker les offres séparément
    offres_hellowork = []
    offres_glassdoor = []

    # Scraper chaque site selon sa structure
    for site in job_sites:
        driver.get(site)
        time.sleep(30)  # Attendre le chargement du site
        print(f"✅ Scraping sur {site}...")
        offres = []

        if "hellowork" in site:
            offres = scrape_hellowork(driver)
            for offre in offres:
                print(f"Titre: {offre[0]}, Lien: {offre[1]}")
                offres_hellowork.append({"Titre": offre[0], "Lien": offre[1]})

        elif "glassdoor" in site:
            offres = scrape_GlassDoor(driver)
            for offre in offres:
                print(f"Titre: {offre['title']}, Lien: {offre['link']}")
                offres_glassdoor.append({"Titre": offre["title"], "Lien": offre["link"]})

    # Sauvegarder les offres HelloWork dans un fichier JSON
    with open(json_filename_hellowork, "w", encoding="utf-8") as json_file:
        json.dump(offres_hellowork, json_file, ensure_ascii=False, indent=4)

    # Sauvegarder les offres Glassdoor dans un fichier JSON
    with open(json_filename_glassdoor, "w", encoding="utf-8") as json_file:
        json.dump(offres_glassdoor, json_file, ensure_ascii=False, indent=4)

finally:
    time.sleep(10)  # Pause finale avant fermeture
    driver.quit()

print(f"📁 Les offres HelloWork ont été enregistrées dans {json_filename_hellowork}")
print(f"📁 Les offres Glassdoor ont été enregistrées dans {json_filename_glassdoor}")


