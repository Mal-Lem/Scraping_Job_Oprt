from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_indeed_details(driver, url):
    print("bien rentrer dans la fonction")
    driver.get(url)
    details = {}

    try:
        # Attendre que la page soit bien chargée
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.jobsearch-JobInfoHeader-title")))


        # Attendre et récupérer à nouveau les éléments après le chargement
        contract_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.css-1h7a62l.eu4oa1w0"))
        )
        print("type contrat " +contract_element.text.strip())
        details['contract_type'] = contract_element.text if contract_element else "Type de contrat non disponible"

        company_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.css-1gcjz36"))
        )
        print("dans la compagnie "+company_element.text.strip())
        details['company'] = company_element.text if company_element else "Entreprise non disponible"

        location_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.css-1vysp2z"))
        )
        print("situer à "+location_element.text.strip())
        details['location'] = location_element.text if location_element else "Localisation non disponible"

        skills_elements = driver.find_elements(By.CSS_SELECTOR, "span.js-match-insights-provider-4pmm6z")
        if skills_elements:  # Vérifie si on a trouvé des compétences
          skills_list = [e.text.strip() for e in skills_elements if e.text.strip()]
          print("✅ Les compétences demandées sont :", ", ".join(skills_list))
          details['skills'] = ", ".join(skills_list)
        else:
          print("⚠ Aucune compétence trouvée.")
          details['skills'] = "Compétences non disponibles"
        education_elements = driver.find_elements(By.CSS_SELECTOR, "span.js-match-insights-provider-4pmm6z")
        if education_elements:  # Vérifie si on a trouvé des compétences
          education_list = [e.text.strip() for e in education_elements if e.text.strip()]
          print("✅ Les compétences demandées sont :", ", ".join(education_list))
          details['education'] = ", ".join(education_list)
        else:
          print("⚠ Aucune compétence trouvée.")
          details['education'] = "Compétences non disponibles"

        # Extraire les sections de détails (Description, Missions, Profil)
        # sections = driver.find_elements(By.CSS_SELECTOR, "div.jobDescriptionText")
        # details['description'] = ", ".join([e.text for e in sections]) if sections else "description non disponible"

        print("et ce que t'as trouvez les details de l'offre ?")

    except Exception as e:
        print(f"⚠ Erreur lors de l'extraction des détails de l'offre Indeed : {e}")

    return details

def scrape_indeed(driver):
    """
    Extrait les liens des offres et accède à chaque lien pour récupérer les détails.
    """
    print("🟠 Détection: Indeed")
    offres = []
    
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.jcs-JobTitle.css-1baag51.eu4oa1w0")))
        job_elements = driver.find_elements(By.CSS_SELECTOR, "a.jcs-JobTitle.css-1baag51.eu4oa1w0")
        for job in job_elements:
            # Extraire le titre de l'offre
            title = job.text
            link = job.get_attribute("href")

            # Récupérer les détails de l'offre
            details = scrape_indeed_details(driver, link)
            offres.append({
                'title': title,
                'link': link,
                'details': details
            })
            
    except Exception as e:
        print(f"⚠ Erreur Indeed : {e}")
    
    return offres
