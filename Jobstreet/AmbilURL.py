from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

# Keywords yang akan di-scrape secara berurutan
KEYWORDS = [
    "Business Analyst",
    "Project Manager", 
    "Business Development",
    "Operations Manager",
    "Sales Executive",
    "Account Executive",
    "Partnership Manager",
    "Consultant",
    "Product Owner",
    "Scrum Master",
    "Strategy Analyst"
]

def keyword_to_url_format(keyword):
    """Convert keyword ke format URL jobstreet"""
    return keyword.lower().replace(" ", "-")

def random_delay(min_sec=0.2, max_sec=0.8):
    delay = random.uniform(min_sec, max_sec)
    print(f"⏳ Waiting {delay:.1f} seconds...")
    time.sleep(delay)

def scrape_keyword(keyword):
    """Scrape semua job links untuk keyword tertentu"""
    print(f"\n{'='*60}")
    print(f"🎯 STARTING SCRAPING FOR: {keyword}")
    print(f"{'='*60}")
    
    url_format = keyword_to_url_format(keyword)
    
    options = Options()
    # options.add_argument("--headless")  # Untuk debug, bisa dimatikan dulu
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.7204.101 Safari/537.36")
    service = Service(r"C:\Users\DEMO PAMERAN\OneDrive\Documents\chromedriver-win64\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    jobs_data = []
    page_num = 1  

    try:
        while True:  # Loop sampai tidak ada job lagi
            # URL untuk setiap halaman
            if page_num == 1:
                url = f"https://id.jobstreet.com/id/{url_format}-jobs"
            else:
                url = f"https://id.jobstreet.com/id/{url_format}-jobs?page={page_num}"
            
            print(f"\n📄 Processing page {page_num}: {url}")
            driver.get(url)
            
            # Delay loading halaman
            print("🔄 Waiting for page to load...")
            random_delay(0.5, 1.0)

            # Ambil semua job card di halaman saat ini
            job_cards = driver.find_elements(By.CSS_SELECTOR, 'article[data-automation="normalJob"]')
            print(f"✅ Total job cards di halaman {page_num}: {len(job_cards)}")
            
            if len(job_cards) == 0:
                print(f"❌ Tidak ada job card di halaman {page_num}. Selesai untuk '{keyword}'.")
                break

            for idx, card in enumerate(job_cards):
                print(f"🔄 Processing card {idx+1} of {len(job_cards)} (Page {page_num})")
                driver.execute_script("arguments[0].scrollIntoView();", card)
                random_delay(0.2, 0.4)  # Delay setelah scroll - dipercepat
                driver.execute_script("arguments[0].click();", card)
                
                # Delay setelah klik card - dipercepat
                print("⏳ Waiting for job details panel...")
                random_delay(0.5, 1.0)

                # Cari dan klik tombol "Tab baru"
                try:
                    new_tab_button = driver.find_element(By.ID, "newTabButton")
                    original_tabs = driver.window_handles
                    
                    # Klik tombol tab baru
                    driver.execute_script("arguments[0].click();", new_tab_button)
                    random_delay(0.3, 0.6)
                    
                    # Tunggu tab baru muncul
                    WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > len(original_tabs))
                    
                    # Pindah ke tab baru
                    new_tab = [tab for tab in driver.window_handles if tab not in original_tabs][0]
                    driver.switch_to.window(new_tab)
                    job_link = driver.current_url
                    
                    # Simpan data
                    jobs_data.append({
                        "Link": job_link,
                        "Keyword": keyword
                    })
                    
                    # Tutup tab baru dan kembali ke tab utama
                    driver.close()
                    driver.switch_to.window(original_tabs[0])
                    
                    print(f"✅ [{len(jobs_data)}] Link berhasil diambil untuk '{keyword}'")
                    
                    if idx < len(job_cards) - 1:  
                        print("⏳ Preparing for next job...")
                        random_delay(0.2, 0.5)
                    
                except Exception as e:
                    print(f"❌ Gagal mengambil link untuk card {idx+1}: {e}")
                    continue
            print(f"🔄 Finished page {page_num} untuk '{keyword}'. Preparing for next page...")
            random_delay(0.5, 1.0)
            
            # Increment halaman untuk iterasi berikutnya
            page_num += 1

    finally:
        driver.quit()

    # Tampilkan summary untuk keyword ini
    if jobs_data:
        print(f"\n📊 SUMMARY untuk '{keyword}':")
        print(f"📄 Total halaman diproses: {page_num-1}")
        print(f"🔗 Total link berhasil diambil: {len(jobs_data)}")
        
        # Simpan ke CSV
        df = pd.DataFrame(jobs_data)
        filename = f"{url_format}.csv"
        df.to_csv(filename, index=False)
        print(f"💾 Data disimpan ke {filename}")
        
        return filename, len(jobs_data)
    else:
        print(f"❌ Tidak ada data untuk '{keyword}'")
        return None, 0

def main():
    """Main function untuk menjalankan scraping semua keywords berurutan"""
    print(f"🚀 STARTING SEQUENTIAL KEYWORD SCRAPER")
    print(f"📋 Keywords: {' → '.join(KEYWORDS)}")
    print(f"⏰ Start time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    total_links = 0
    successful_keywords = []
    failed_keywords = []
    
    for i, keyword in enumerate(KEYWORDS, 1):
        print(f"\n🎯 Progress: {i}/{len(KEYWORDS)} keywords")
        print(f"🔄 Current: {keyword}")
        
        try:
            filename, link_count = scrape_keyword(keyword)
            if filename:
                successful_keywords.append((keyword, filename, link_count))
                total_links += link_count
                print(f"✅ SUCCESS: '{keyword}' completed with {link_count} links")
            else:
                failed_keywords.append(keyword)
                print(f"❌ FAILED: '{keyword}' - no data scraped")
                
        except Exception as e:
            failed_keywords.append(keyword)
            print(f"❌ FAILED: '{keyword}' - Error: {e}")
            
        # Delay antar keyword untuk menghindari rate limiting
        if i < len(KEYWORDS):
            print(f"⏳ Waiting before next keyword...")
            random_delay(1, 2)
    
    # Final summary
    print(f"\n{'='*80}")
    print(f"🎉 SEQUENTIAL SCRAPING COMPLETED!")
    print(f"{'='*80}")
    print(f"⏰ End time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"✅ Successful keywords: {len(successful_keywords)}")
    print(f"❌ Failed keywords: {len(failed_keywords)}")
    print(f"� Total links collected: {total_links}")
    
    if successful_keywords:
        print(f"\n📊 SUCCESSFUL RESULTS:")
        for keyword, filename, count in successful_keywords:
            print(f"  • {keyword}: {count} links → {filename}")
    
    if failed_keywords:
        print(f"\n❌ FAILED KEYWORDS:")
        for keyword in failed_keywords:
            print(f"  • {keyword}")
    
    print(f"\n💡 Files generated: Check CSV files for each successful keyword!")

if __name__ == "__main__":
    main()