from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_wttj(driver):
    print("🟠 Détection: Welcome to the Jungle")
    offres = []
    try:
        # Attente jusqu'à ce que l'élément contenant l'offre soit visible
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.sc-hwFkLi.cORpiU")))
        
        # Trouver tous les éléments contenant des offres
        job_elements = driver.find_elements(By.CSS_SELECTOR, "div.sc-hwFkLi.cORpiU")
        
        for job in job_elements:
            # Extraire le titre de l'offre
            title_element = job.find_element(By.CSS_SELECTOR, "h4.sc-czkgLR")
            title = title_element.text if title_element else "Titre non disponible"
            
            # Extraire le lien de l'offre
            link_element = job.find_element(By.XPATH, ".//a")
            link = link_element.get_attribute("href") if link_element else "Pas de lien"
            
            # Ajouter l'offre à la liste
            offres.append((title, link))

    except Exception as e:
        print(f"⚠ Erreur Welcome to the Jungle: {e}")
    
    return offres
