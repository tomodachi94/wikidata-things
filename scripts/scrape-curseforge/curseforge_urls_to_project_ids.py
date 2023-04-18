import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import sqlite3 # We sometimes need to directly query the database
import random
import requests # Check for 404s and other undesireables

from tomodb import Database # local

driver = webdriver.Firefox() # You can change this to `webdriver.Chrome`, but results may vary

def get_curseforge_id(url: str, driver: webdriver = None):
    """Scrapes the provided CurseForge page for the project identifier."""
    driver.get(url)
    is_404 = ""
    try:
        is_404 = driver.find_element(By.CSS_SELECTOR, ".error-page__message--not-found")
    except:
        pass
    if not is_404:
        tag = driver.find_element(By.CSS_SELECTOR, "div.mb-3:nth-child(2) > div:nth-child(1) > span:nth-child(2)") # Complicated CSS selector to extract the project ID from the HTML; this could change in the future
        return tag.get_attribute("innerHTML"), True
    else:
        print("Bad URL: " + url)
        return None, False


db = Database("urls.sqlite3")

def store_project_ids(driver: webdriver = None):
    conn = sqlite3.connect("./urls.sqlite3")
    c = conn.cursor()
    c.execute("SELECT title, curseforge_url FROM mods WHERE curseforge_project_id IS NULL")
    rows = c.fetchall()
    
    for row in rows:
        title, url = row
        id, is_live = get_curseforge_id(url, driver=driver)
        if is_live:
            try:
                db.update({"title": title, "curseforge_url": url, "curseforge_project_id": id})
                time.sleep(random.randint(2, 4))
            except sqlite3.IntegrityError:
                print(f"IntegrityError: {{'title': title, 'curseforge_url': url, 'curseforge_project_id': id}}")
        else:
            pass
        
        conn.commit()

    conn.close()

store_project_ids(driver=driver)

# We're all done here folks
driver.quit()
db.close()
