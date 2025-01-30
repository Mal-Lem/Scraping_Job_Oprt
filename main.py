from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Importer les modules de scraping
from scraping.indeed import scrape_indeed
from scraping.WelToJungle import scrape_wttj
from scraping.helloWork import scrape_hellowork

# Initialiser WebDriver
service = Service(executable_path="./chromedriver.exe")
driver = webdriver.Chrome(service=service)

try:
    driver.get("https://google.com/")

    # Attendre la barre de recherche
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "gLFyf")))

    # Entrer la requête de recherche
    input_element = driver.find_element(By.CLASS_NAME, "gLFyf")
    input_element.clear()
    time.sleep(2)
    input_element.send_keys("data engineer emploi paris" + Keys.ENTER)

    # Attendre et récupérer les liens des résultats
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[jsname='UWckNb']")))
    links = driver.find_elements(By.CSS_SELECTOR, "a[jsname='UWckNb']")

    job_sites = []
    for link in links[:3]:  # On prend les 3 premiers résultats
        url = link.get_attribute("href")
        title = link.find_element(By.TAG_NAME, "h3").text if link.find_elements(By.TAG_NAME, "h3") else "Sans titre"
        print(f"{title}: {url}")
        job_sites.append(url)

    # Scraper chaque site selon sa structure
    for site in job_sites:
        driver.get(site)
        time.sleep(30)  # Attendre le chargement du site

        print(f"✅ Scraping sur {site}...")

        offres = []

        if "indeed" in site:
            offres = scrape_indeed(driver)
        elif "wttj" in site or "welcometothejungle" in site:
            offres = scrape_wttj(driver)
        elif "hellowork" in site:
            offres = scrape_hellowork(driver)

        # Affichage des offres trouvées
        for offre in offres:
            print(f"🔹 {offre[0]} → {offre[1]}")

finally:
    time.sleep(10)  # Pause finale avant fermeture
    driver.quit()
