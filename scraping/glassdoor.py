import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_GlassDoor(driver):
    """
    Extrait les titres et les liens des offres avec pagination.
    """
    print("🟠 Détection: GlassDoor")
    offres = []
    
    try:
        while True:  # Boucle pour parcourir plusieurs pages
            WebDriverWait(driver, 100).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.JobCard_jobTitle__GLyJ1")))
            job_elements = driver.find_elements(By.CSS_SELECTOR, "a.JobCard_jobTitle__GLyJ1")
            
            for job in job_elements:
                # Extraire le titre de l'offre avec gestion des erreurs
                try:
                    title = job.text
                except Exception as e:
                    print(f"Erreur lors de l'extraction du titre : {e}")
                    title = "Non précisé"
                
                # Extraire le lien vers l'offre
                try:
                    link = job.get_attribute("href")
                except Exception as e:
                    print(f"Erreur lors de l'extraction du lien : {e}")
                    link = "Non précisé"
                
                # Ajouter un petit délai pour éviter d'envoyer trop de requêtes d'un coup
                time.sleep(1)
                    
                # Ajouter l'offre dans la liste
                offres.append({
                    "title": title,
                    "link": link,
                })
            
            # Chercher le bouton ou lien de la page suivante
            try:
                # Sélecteur pour le bouton "Suivant" (à ajuster si nécessaire)
                next_button = driver.find_element(By.CSS_SELECTOR, 'a.pagingNext')  # À adapter si le sélecteur change
                if next_button:
                    next_button.click()  # Clique sur le bouton "Suivant"
                    WebDriverWait(driver, 5).until(EC.staleness_of(job_elements[0]))  # Attendre que la page charge
                else:
                    break  # Si aucun bouton de page suivante n'est trouvé, sortir de la boucle
            except Exception as e:
                print(f"Erreur pagination : {e}")
                break  # En cas d'erreur avec la pagination, sortir de la boucle

    except Exception as e:
        print(f"Erreur générale lors du scraping : {e}")
    
    return offres
