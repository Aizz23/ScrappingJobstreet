import pandas as pd
import os
import glob

def merge_all_categories():
    """
    Menggabungkan SEMUA file CSV dari SEMUA kategori menjadi satu file besar
    dan menghapus duplikat URL
    """
    
    # Base directory
    base_dir = r"c:\Users\DEMO PAMERAN\Downloads\Semester 4\Jobstreet"
    
    print("🚀 MERGING ALL CSV FILES FROM ALL CATEGORIES")
    print("="*70)
    print(f"📂 Base directory: {base_dir}")
    
    # List semua folder kategori
    category_folders = [
        "Business & Management",
        "Customer Support", 
        "Design & Architecture",
        "Education ad Training",
        "F&B & hospitality",
        "Finance & Legal",
        "Healtcare",
        "Manufacturing dan logistic",
        "Tech and Data",
        "Ui Ux"
    ]
    
    # Juga cari file CSV langsung di root directory
    all_csv_files = []
    
    # Ambil file CSV dari root directory
    root_csv_files = glob.glob(os.path.join(base_dir, "*.csv"))
    if root_csv_files:
        print(f"\n📁 ROOT DIRECTORY - Found {len(root_csv_files)} CSV files:")
        for file in root_csv_files:
            filename = os.path.basename(file)
            # Skip file yang merupakan hasil merge sebelumnya
            if not any(skip in filename.lower() for skip in ['combined', 'merged', 'all_scraped', 'backup']):
                all_csv_files.append((file, "ROOT"))
                print(f"  • {filename}")
    
    # Ambil file CSV dari setiap folder kategori
    for category in category_folders:
        category_path = os.path.join(base_dir, category)
        
        if os.path.exists(category_path):
            csv_files = glob.glob(os.path.join(category_path, "*.csv"))
            
            if csv_files:
                print(f"\n📁 {category} - Found {len(csv_files)} CSV files:")
                for file in csv_files:
                    filename = os.path.basename(file)
                    # Skip file yang merupakan hasil merge sebelumnya
                    if not any(skip in filename.lower() for skip in ['combined', 'merged', 'all_scraped', 'backup', 'no_duplicate']):
                        all_csv_files.append((file, category))
                        print(f"  • {filename}")
        else:
            print(f"\n⚠️  {category} folder not found, skipping...")
    
    if not all_csv_files:
        print("\n❌ No CSV files found in any category!")
        return
    
    print(f"\n📊 TOTAL FILES TO PROCESS: {len(all_csv_files)}")
    
    # List untuk menyimpan semua dataframe
    all_dataframes = []
    total_rows_before = 0
    category_stats = {}
    
    print(f"\n🔄 Processing each file...")
    
    for file_path, category in all_csv_files:
        try:
            filename = os.path.basename(file_path)
            print(f"\n📋 Processing: {category}/{filename}")
            
            # Baca CSV
            df = pd.read_csv(file_path)
            rows_count = len(df)
            total_rows_before += rows_count
            
            # Tambahkan kolom metadata
            df['Source_File'] = filename.replace('.csv', '')
            df['Category'] = category
            
            # Update category stats
            if category not in category_stats:
                category_stats[category] = {'files': 0, 'rows': 0}
            category_stats[category]['files'] += 1
            category_stats[category]['rows'] += rows_count
            
            print(f"  ✅ Loaded {rows_count:,} rows")
            print(f"  📋 Columns: {list(df.columns)}")
            
            all_dataframes.append(df)
            
        except Exception as e:
            print(f"  ❌ Error reading {category}/{filename}: {e}")
            continue
    
    if not all_dataframes:
        print("❌ No valid CSV files found to merge!")
        return
    
    # Gabungkan semua dataframe
    print(f"\n🔗 Combining all dataframes...")
    merged_df = pd.concat(all_dataframes, ignore_index=True)
    print(f"📊 Total rows after merging: {len(merged_df):,}")
    
    # Hapus duplikat berdasarkan Link/URL
    print(f"\n🔍 Checking for duplicate URLs...")
    
    # Cek kolom yang mungkin berisi URL
    url_columns = []
    for col in merged_df.columns:
        if any(keyword in col.lower() for keyword in ['link', 'url', 'href']):
            url_columns.append(col)
    
    print(f"🔗 URL columns found: {url_columns}")
    
    duplicates_removed = 0
    if url_columns:
        # Gunakan kolom URL pertama yang ditemukan
        url_column = url_columns[0]
        initial_count = len(merged_df)
        
        # Hapus duplikat berdasarkan URL
        merged_df = merged_df.drop_duplicates(subset=[url_column], keep='first')
        final_count = len(merged_df)
        duplicates_removed = initial_count - final_count
        
        print(f"✅ Removed {duplicates_removed:,} duplicate URLs")
        print(f"📊 Final count: {final_count:,} unique rows")
    else:
        print("⚠️  No URL column found, skipping duplicate removal")
    
    # Urutkan data
    if 'Category' in merged_df.columns and 'Keyword' in merged_df.columns:
        merged_df = merged_df.sort_values(['Category', 'Keyword', 'Source_File'])
        print("📋 Data sorted by Category, Keyword, and Source File")
    elif 'Category' in merged_df.columns:
        merged_df = merged_df.sort_values(['Category', 'Source_File'])
        print("📋 Data sorted by Category and Source File")
    
    # Reset index
    merged_df = merged_df.reset_index(drop=True)
    
    # Simpan hasil gabungan
    output_path = os.path.join(base_dir, "ALL_SCRAPED_JOBSTREET_COMBINED.csv")
    merged_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    
    print(f"\n{'='*70}")
    print(f"🎉 MEGA MERGE COMPLETED!")
    print(f"{'='*70}")
    print(f"📁 Output file: ALL_SCRAPED_JOBSTREET_COMBINED.csv")
    print(f"📊 Final rows: {len(merged_df):,}")
    print(f"📋 Total files merged: {len(all_csv_files)}")
    print(f"🗑️  Duplicates removed: {duplicates_removed:,}")
    print(f"💾 File size: ~{len(merged_df) * 0.5 / 1000:.1f} MB (estimated)")
    
    # Tampilkan breakdown per kategori
    print(f"\n📈 BREAKDOWN BY CATEGORY:")
    final_category_counts = merged_df['Category'].value_counts() if 'Category' in merged_df.columns else {}
    for category, stats in category_stats.items():
        final_count = final_category_counts.get(category, 0)
        print(f"  • {category}:")
        print(f"    - Files: {stats['files']}")
        print(f"    - Original rows: {stats['rows']:,}")
        print(f"    - Final unique rows: {final_count:,}")
    
    # Tampilkan breakdown per keyword (top 20)
    if 'Keyword' in merged_df.columns:
        print(f"\n📊 TOP 20 KEYWORDS BY COUNT:")
        keyword_counts = merged_df['Keyword'].value_counts().head(20)
        for keyword, count in keyword_counts.items():
            print(f"  • {keyword}: {count:,} links")
    
    # Tampilkan kolom yang tersedia
    print(f"\n📝 COLUMNS IN FINAL FILE:")
    for col in merged_df.columns:
        print(f"  • {col}")
    
    print(f"\n💡 TIPS:")
    print(f"  • File saved in main directory: {base_dir}")
    print(f"  • Contains data from ALL categories")
    print(f"  • No duplicate URLs")
    print(f"  • Ready for analysis or further processing!")
    
    return output_path, len(merged_df), len(all_csv_files), duplicates_removed

if __name__ == "__main__":
    print("🌟 STARTING MEGA CSV MERGE OPERATION")
    print("🎯 Goal: Combine ALL CSV files from ALL categories")
    print("🧹 Remove duplicates and organize data")
    
    try:
        output_file, total_rows, files_merged, duplicates = merge_all_categories()
        
        print(f"\n🎊 MEGA SUCCESS!")
        print(f"📄 File: ALL_SCRAPED_JOBSTREET_COMBINED.csv")
        print(f"📊 Total unique rows: {total_rows:,}")
        print(f"📁 Files merged: {files_merged}")
        print(f"🗑️  Duplicates removed: {duplicates:,}")
        print(f"\n🎉 Your complete JobStreet dataset is ready!")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("💡 Check if folders exist and contain CSV files")
        import traceback
        traceback.print_exc()
