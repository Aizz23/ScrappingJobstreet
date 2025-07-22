import pandas as pd
from multiprocessing import Pool
from tqdm import tqdm

from main_scraper import scrape_job 
import os

# === Load file CSV ===
# Pastikan menggunakan path absolut
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "ALL_SCRAPED_JOBSTREET_COMBINED.csv")

# Cek apakah file ada
if not os.path.exists(csv_path):
    print(f"❌ File tidak ditemukan: {csv_path}")
    print("💡 Jalankan mega_merge_all.py terlebih dahulu untuk membuat file ALL_SCRAPED_JOBSTREET_COMBINED.csv")
    exit()

df = pd.read_csv(csv_path)
print(f"📊 Loaded {len(df)} total job links from ALL categories")
print(f"📋 Columns available: {list(df.columns)}")

# Tampilkan breakdown per kategori
if 'Category' in df.columns:
    print(f"\n📈 BREAKDOWN BY CATEGORY:")
    category_counts = df['Category'].value_counts()
    for category, count in category_counts.items():
        print(f"  • {category}: {count:,} links")

urls = df["Link"].tolist()

# === PRODUCTION MODE: Scrape SEMUA link ===
print(f"\n🚀 PRODUCTION MODE: Processing ALL {len(urls):,} links")
print(f"⚠️  This will take a VERY long time!")
print(f"💡 Consider running in batches")

# Pilihan batch size
print(f"\n📋 BATCH OPTIONS:")
print(f"1. Full run ({len(urls):,} links) - VERY SLOW")
print(f"2. Test batch (100 links) - Quick test")
print(f"3. Small batch (500 links) - Reasonable")
print(f"4. Medium batch (1000 links) - Moderate")
print(f"5. Large batch (5000 links) - Long run")

try:
    choice = input("Choose option (1-5): ").strip()
    
    if choice == "1":
        batch_size = len(urls)
        print(f"🎯 Selected: FULL RUN with {batch_size:,} links")
    elif choice == "2":
        batch_size = 100
        print(f"🎯 Selected: TEST BATCH with {batch_size} links")
    elif choice == "3":
        batch_size = 500
        print(f"🎯 Selected: SMALL BATCH with {batch_size} links")
    elif choice == "4":
        batch_size = 1000
        print(f"🎯 Selected: MEDIUM BATCH with {batch_size} links")
    elif choice == "5":
        batch_size = 5000
        print(f"🎯 Selected: LARGE BATCH with {batch_size} links")
    else:
        print("Invalid choice, defaulting to TEST BATCH (100 links)")
        batch_size = 100
        
except KeyboardInterrupt:
    print("\n❌ Cancelled by user")
    exit()

# Gunakan batch yang dipilih
all_urls = urls[:batch_size]
print(f"\n🎯 Will process {len(all_urls):,} job links")

# === Fungsi pembungkus ===
def scrape_with_index(args):
    index, url = args
    print(f"🔄 Scraping {index+1}: {url}")
    result = scrape_job(url)
    result["index"] = index + 1
    return result

# === Parallel scraping ===
if __name__ == "__main__":
    # Buat inputs dengan index untuk ALL URLs
    inputs = list(enumerate(all_urls))
    
    print(f"🚀 Starting FULL scraping of {len(all_urls):,} links...")
    print(f"💾 Results will be saved every 1000 completed jobs")
    
    # Untuk production, jalankan sequential dengan progress tracking
    results = []
    failed_count = 0
    
    for i, input_data in enumerate(inputs, 1):
        try:
            result = scrape_with_index(input_data)
            results.append(result)
            
            # Progress update setiap 50 jobs
            if i % 50 == 0:
                print(f"📊 Progress: {i}/{len(all_urls)} ({i/len(all_urls)*100:.1f}%) - Success: {len(results)}, Failed: {failed_count}")
            
            # Auto-save setiap 1000 jobs
            if i % 1000 == 0:
                df_temp = pd.DataFrame(results)
                temp_path = os.path.join(script_dir, f"all_scraped_detail_backup_{i}.csv")
                df_temp.to_csv(temp_path, index=False, encoding="utf-8-sig")
                print(f"💾 Backup saved: {temp_path} ({len(results):,} jobs completed)")
                
        except Exception as e:
            failed_count += 1
            print(f"❌ Failed to scrape job {i}: {e}")
            continue

    # Final save
    df_result = pd.DataFrame(results)
    output_path = os.path.join(script_dir, "ALL_SCRAPED_JOBSTREET_DETAILS.csv")
    df_result.to_csv(output_path, index=False, encoding="utf-8-sig")
    
    print(f"\n{'='*70}")
    print(f"🎉 FULL SCRAPING COMPLETED!")
    print(f"{'='*70}")
    print(f"✅ Total successful: {len(results):,}")
    print(f"❌ Total failed: {failed_count:,}")
    print(f"📊 Success rate: {len(results)/(len(results)+failed_count)*100:.1f}%")
    print(f"💾 Final file: ALL_SCRAPED_JOBSTREET_DETAILS.csv")
    print(f"📈 File contains detailed job information from ALL categories")
    print(f"🎯 Ready for analysis, filtering, or further processing!")
