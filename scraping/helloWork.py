from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_hellowork(driver):
    print("🔵 Détection: HelloWork")
    offres = []
    try:
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-cy="offerTitle"]')))
        job_elements = driver.find_elements(By.CSS_SELECTOR, 'a[data-cy="offerTitle"]')
        for job in job_elements:
            title = job.find_element(By.TAG_NAME, "h3").text if job.find_elements(By.TAG_NAME, "h3") else "Sans titre"
            link = job.get_attribute("href")
            offres.append((title, link))
            
    except Exception as e:
        print(f"⚠ Erreur HelloWork: {e}")
    
    return offres
