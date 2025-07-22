import pandas as pd
import os
import glob

def merge_customer_support_csv():
    """
    Menggabungkan semua file CSV di folder Customer Support menjadi satu file
    dan sekaligus menghapus duplikat URL
    """
    
    # Path ke folder Customer Support
    customer_support_folder = r"c:\Users\DEMO PAMERAN\Downloads\Semester 4\Jobstreet\Customer Support"
    
    print("🚀 MERGING CUSTOMER SUPPORT CSV FILES")
    print("="*60)
    print(f"📂 Target folder: {customer_support_folder}")
    
    # Cari semua file CSV di folder
    csv_files = glob.glob(os.path.join(customer_support_folder, "*.csv"))
    
    print(f"\n🔍 Found {len(csv_files)} CSV files:")
    for file in csv_files:
        filename = os.path.basename(file)
        print(f"  • {filename}")
    
    if not csv_files:
        print("❌ No CSV files found in Customer Support folder!")
        return
    
    # List untuk menyimpan semua dataframe
    all_dataframes = []
    total_rows_before = 0
    
    print(f"\n📊 Processing each file...")
    
    for file_path in csv_files:
        try:
            filename = os.path.basename(file_path)
            print(f"\n🔄 Processing: {filename}")
            
            # Baca CSV
            df = pd.read_csv(file_path)
            rows_count = len(df)
            total_rows_before += rows_count
            
            # Tambahkan kolom source file untuk tracking
            df['Source_File'] = filename.replace('.csv', '')
            
            print(f"  ✅ Loaded {rows_count} rows")
            
            # Tampilkan kolom yang ada
            print(f"  📋 Columns: {list(df.columns)}")
            
            all_dataframes.append(df)
            
        except Exception as e:
            print(f"  ❌ Error reading {filename}: {e}")
            continue
    
    if not all_dataframes:
        print("❌ No valid CSV files found to merge!")
        return
    
    # Gabungkan semua dataframe
    print(f"\n🔗 Combining all dataframes...")
    merged_df = pd.concat(all_dataframes, ignore_index=True)
    print(f"📊 Total rows after merging: {len(merged_df)}")
    
    # Hapus duplikat berdasarkan Link/URL
    print(f"\n🔍 Checking for duplicate URLs...")
    
    # Cek kolom yang mungkin berisi URL
    url_columns = []
    for col in merged_df.columns:
        if any(keyword in col.lower() for keyword in ['link', 'url', 'href']):
            url_columns.append(col)
    
    print(f"🔗 URL columns found: {url_columns}")
    
    if url_columns:
        # Gunakan kolom URL pertama yang ditemukan
        url_column = url_columns[0]
        initial_count = len(merged_df)
        
        # Hapus duplikat berdasarkan URL
        merged_df = merged_df.drop_duplicates(subset=[url_column], keep='first')
        final_count = len(merged_df)
        duplicates_removed = initial_count - final_count
        
        print(f"✅ Removed {duplicates_removed} duplicate URLs")
        print(f"📊 Final count: {final_count} unique rows")
    else:
        print("⚠️  No URL column found, skipping duplicate removal")
    
    # Urutkan data
    if 'Keyword' in merged_df.columns:
        merged_df = merged_df.sort_values(['Keyword', 'Source_File'])
        print("📋 Data sorted by Keyword and Source File")
    elif 'Source_File' in merged_df.columns:
        merged_df = merged_df.sort_values('Source_File')
        print("📋 Data sorted by Source File")
    
    # Reset index
    merged_df = merged_df.reset_index(drop=True)
    
    # Simpan hasil gabungan
    output_path = os.path.join(customer_support_folder, "CustomerSupport_Combined_NoDuplicates.csv")
    merged_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    
    print(f"\n{'='*60}")
    print(f"🎉 MERGE & DEDUPLICATION COMPLETED!")
    print(f"{'='*60}")
    print(f"📁 Output file: CustomerSupport_Combined_NoDuplicates.csv")
    print(f"📊 Final rows: {len(merged_df)}")
    print(f"📋 Files merged: {len(all_dataframes)}")
    print(f"🗑️  Duplicates removed: {duplicates_removed if url_columns else 0}")
    
    # Tampilkan summary per file
    if 'Source_File' in merged_df.columns:
        print(f"\n📈 BREAKDOWN BY SOURCE FILE:")
        file_counts = merged_df['Source_File'].value_counts().sort_index()
        for source_file, count in file_counts.items():
            print(f"  • {source_file}: {count} unique rows")
    
    # Tampilkan summary per keyword (jika ada)
    if 'Keyword' in merged_df.columns:
        print(f"\n📊 BREAKDOWN BY KEYWORD:")
        keyword_counts = merged_df['Keyword'].value_counts()
        for keyword, count in keyword_counts.items():
            print(f"  • {keyword}: {count} unique rows")
    
    # Tampilkan kolom yang tersedia
    print(f"\n📝 COLUMNS IN FINAL FILE:")
    for col in merged_df.columns:
        print(f"  • {col}")
    
    print(f"\n💡 The combined file is saved in the Customer Support folder!")
    return output_path, len(merged_df)

if __name__ == "__main__":
    try:
        output_file, total_rows = merge_customer_support_csv()
        print(f"\n✅ SUCCESS!")
        print(f"📄 File: NoDuplicate.csv")
        print(f"📊 Total unique rows: {total_rows}")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("💡 Make sure the Customer Support folder exists and contains CSV files")
