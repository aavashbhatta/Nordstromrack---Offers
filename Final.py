import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.options import Options
import time
import random

def extract_text():
    # Set up the Edge WebDriver with headless mode and disabled GPU
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)
    
    try:
        # Open the URL
        driver.get('https://www.nordstromrack.com/events/all?breadcrumb=Home%2FFlash%20Events')
        
        # Random delay to mimic human behavior
        time.sleep(random.uniform(3, 5))
        
        # Wait for the page to load fully and all elements with the specific class
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.udmGE.cSeCo.wHJLP.L1fU8'))
        )
        
        # Random delay to mimic human behavior
        time.sleep(random.uniform(2, 4))
        
        # Extract the text from all matching <div> elements
        specific_div_texts = [element.text for element in driver.find_elements(By.CSS_SELECTOR, '.udmGE.cSeCo.wHJLP.L1fU8') if "Event ends" not in element.text]
        
        # Debug: print the length of the extracted texts
        for i, text in enumerate(specific_div_texts, 1):
            print(f"Extracted text length {i}: {len(text)}")
        
        # Return only the first ten texts
        return specific_div_texts[:15]
    
    except Exception as e:
        return f"Error: {e}"
    
    finally:
        # Close the driver
        driver.quit()

def save_to_json(data):
    store_id = 5041
    formatted_data = [{"storeId": store_id, "title": title} for title in data]
    
    with open('extracted_data.json', 'w') as json_file:
        json.dump(formatted_data, json_file, indent=4)

# Extract texts
extracted_texts = extract_text()

# Save to JSON
if isinstance(extracted_texts, list):
    save_to_json(extracted_texts)
else:
    print(extracted_texts)
