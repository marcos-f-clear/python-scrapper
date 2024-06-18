from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.http import HttpResponse
from bs4 import BeautifulSoup
from django.http import JsonResponse
import requests
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options


def scrape_json(request):
  next_page_url = "https://www.capterra.com/customer-relationship-management-software/"
  
  s = Service(ChromeDriverManager().install())
  options = Options()
  driver = uc.Chrome(options=options)

  driver.get(next_page_url)

  content = driver.page_source
  
  softwares = []
  
  soup = BeautifulSoup(content, 'html.parser')
  
  print(soup)

  container = soup.find(attrs={"data-testid": "product-card-stack"})
  
  
  if container:
    elements = container.select("[id^=product-card-container]")
    for element in elements:
      software = {}
      logo_container = element.find("figure")
      print(logo_container)
      
      if logo_container:
        logo = logo_container.find("img")
        if logo:
          software["logo"] = logo["src"]
      
      name_container = element.find("h2")
      if name_container:
        software["name"] = name_container.text
      softwares.append(software)
          
    driver.quit()
    if softwares:
      return JsonResponse(softwares, safe=False)
    else:
     return JsonResponse({"error": "No data found"})
