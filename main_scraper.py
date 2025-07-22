from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import random

def create_driver():
    """Membuat driver Chrome dengan konfigurasi optimal untuk speed"""
    options = Options()
    options.add_argument("--headless")  # Jalankan tanpa GUI untuk speed
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.7204.101 Safari/537.36")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-logging")
    options.add_argument("--silent")
    options.add_argument("--disable-images")  # Tidak load gambar untuk speed
    options.add_argument("--disable-javascript")  # Tidak perlu JS untuk scraping
    options.add_argument("--disable-css")  # Tidak perlu CSS untuk scraping
    options.add_argument("--disable-plugins")
    options.add_argument("--disable-notifications")
    
    service = Service(r"C:\Users\DEMO PAMERAN\OneDrive\Documents\chromedriver-win64\chromedriver.exe")
    return webdriver.Chrome(service=service, options=options)

def scrape_job(url):
    """Scrape detail job dari URL Jobstreet"""
    driver = None
    try:
        driver = create_driver()
        driver.get(url)
        
        # Wait for page to load - dipercepat
        time.sleep(random.uniform(0.5, 1.0))
        
        # Get page source and parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Inisialisasi result
        result = {
            "url": url,
            "job_title": "",
            "company_name": "",
            "location": "",
            "posted_date": "",
            "employment_type": "",
            "salary": "",
            "job_description": "",
            "requirements": ""
        }
        
        # Scrape Job Title
        try:
            title_elem = soup.find('h1', {'data-automation': 'job-detail-title'})
            if title_elem:
                result["job_title"] = title_elem.get_text(strip=True)
        except:
            pass
        
        # Scrape Company Name
        try:
            company_elem = soup.find('span', {'data-automation': 'advertiser-name'})
            if company_elem:
                result["company_name"] = company_elem.get_text(strip=True)
        except:
            pass
        
        # Scrape Location
        try:
            location_elem = soup.find('span', {'data-automation': 'job-detail-location'})
            if location_elem:
                result["location"] = location_elem.get_text(strip=True)
        except:
            pass
        
        # Scrape Posted Date - perbaiki berdasarkan HTML sebenarnya
        try:
            date_selectors = [
                'time',                                               
                '[data-automation="job-detail-date"]',               
                'span:contains("Posted")',                           
                'span:contains("hari yang lalu")',                   
                'span:contains("minggu yang lalu")',                 
                'span:contains("bulan yang lalu")',                  
                'span:contains("ago")',                              
                '.posted-date'                                       
            ]
            
            for selector in date_selectors:
                date_elements = soup.select(selector)
                for elem in date_elements:
                    date_text = elem.get('datetime', '') or elem.get_text(strip=True)
                    if date_text and any(keyword in date_text.lower() for keyword in ['posted', 'hari yang lalu', 'minggu yang lalu', 'bulan yang lalu', 'ago', 'yesterday', 'today']):
                        # Clean date text dari karakter yang bisa merusak CSV
                        cleaned_date = ' '.join(date_text.split())  # Remove extra spaces/newlines
                        result["posted_date"] = cleaned_date
                        break
                if result["posted_date"]:
                    break
        except:
            pass

        # Scrape Employment Type - 
        try:
            emp_type_selectors = [
                'span[data-automation="job-detail-work-type"] a',  
                'span[data-automation="job-detail-work-type"]',    
                'div[data-automation="job-detail-classifications"] a',  
                'div[data-automation="job-detail-classifications"] span', 
                '[data-testid="job-detail-work-arrangement"]'
            ]
            
            for selector in emp_type_selectors:
                emp_elements = soup.select(selector)
                for elem in emp_elements:
                    text = elem.get_text(strip=True)
                    # Deteksi employment type berdasarkan kata kunci
                    if any(word in text.lower() for word in ['full time', 'full-time', 'part time', 'part-time', 'contract', 'permanent', 'internship', 'freelance', 'temporary']):
                        result["employment_type"] = text
                        break
                if result["employment_type"]:
                    break
        except:
            pass
        
        # Scrape Salary - 
        try:
            # Hanya cari selector utama yang pasti mengandung salary
            salary_selectors = [
                'span[data-automation="job-detail-salary"]',          
                '[data-testid="job-detail-salary"]',                  
                'div[data-automation="job-detail-salary"]'            
            ]
            
            for selector in salary_selectors:
                salary_elem = soup.select_one(selector)
                if salary_elem:
                    salary_text = salary_elem.get_text(strip=True)
                    # Hanya ambil jika benar-benar mengandung informasi gaji
                    if any(currency in salary_text.lower() for currency in ['rp', 'idr', 'rupiah']) or any(pattern in salary_text for pattern in ['$', '€', '£']):
                        result["salary"] = salary_text
                        break
        except:
            pass
        
        
        # Scrape Job Description - Conservative approach (aman) - dipercepat
        try:
            desc_elem = soup.find('div', {'data-automation': 'jobAdDetails'})
            if desc_elem:
                # Remove script, style, dan elemen yang tidak diinginkan
                for unwanted in desc_elem(["script", "style", "nav", "footer", "header"]):
                    unwanted.decompose()
                
                # Ambil semua content sebagai job description - dipercepat dengan limit lebih kecil
                text = desc_elem.get_text(separator=' ', strip=True)  # Gunakan space, bukan newline
                # Clean up multiple spaces dan karakter yang bisa merusak CSV
                cleaned_text = ' '.join(text.split())  # Menggabungkan multiple spaces jadi satu
                result["job_description"] = cleaned_text[:1500]  # Limit diperkecil untuk speed
                
                # Requirements tetap kosong (conservative approach)
                result["requirements"] = ""
                
        except:
            pass
        
        return result
        
    except Exception as e:
        return {
            "url": url,
            "job_title": "",
            "company_name": "",
            "location": "",
            "posted_date": "",
            "employment_type": "",
            "salary": "",
            "job_description": "",
            "requirements": ""
        }
           
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

if __name__ == "__main__":
    # Test dengan satu URL
    test_url = "https://id.jobstreet.com/id/job/85531806?ref=search-standalone&type=standard&origin=showNewTab#sol=7733c07e6a9b54d6c666d6b526a92c9a2d652666"
    result = scrape_job(test_url)
    print("Test result:")
    for key, value in result.items():
        print(f"{key}: {value}")
