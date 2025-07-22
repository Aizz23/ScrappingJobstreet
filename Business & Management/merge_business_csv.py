import pandas as pd
import os
import glob

def merge_business_csv():
    """Menggabungkan semua file CSV di folder Business & Management menjadi satu file"""
    
    # Path ke folder Business & Management
    business_folder = r"c:\Users\DEMO PAMERAN\Downloads\Semester 4\Jobstreet\Business & Management"
    
    # Cari semua file CSV di folder
    csv_files = glob.glob(os.path.join(business_folder, "*.csv"))
    
    print(f"🔍 Found {len(csv_files)} CSV files in Business & Management folder:")
    for file in csv_files:
        filename = os.path.basename(file)
        print(f"  • {filename}")
    
    # List untuk menyimpan semua dataframe
    all_dataframes = []
    
    print(f"\n📊 Merging CSV files...")
    
    for file_path in csv_files:
        try:
            filename = os.path.basename(file_path)
            print(f"🔄 Processing: {filename}")
            
            # Baca CSV
            df = pd.read_csv(file_path)
            
            # Tambahkan kolom source file untuk tracking
            df['Source_File'] = filename.replace('.csv', '')
            
            print(f"  ✅ Loaded {len(df)} rows from {filename}")
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
    
    # Hapus duplikat berdasarkan Link (jika ada)
    initial_count = len(merged_df)
    if 'Link' in merged_df.columns:
        merged_df = merged_df.drop_duplicates(subset=['Link'], keep='first')
        final_count = len(merged_df)
        print(f"📋 Removed {initial_count - final_count} duplicate links")
    
    # Urutkan berdasarkan keyword atau source file
    if 'Keyword' in merged_df.columns:
        merged_df = merged_df.sort_values(['Keyword', 'Source_File'])
    else:
        merged_df = merged_df.sort_values('Source_File')
    
    # Reset index
    merged_df = merged_df.reset_index(drop=True)
    
    # Simpan hasil gabungan
    output_path = r"c:\Users\DEMO PAMERAN\Downloads\Semester 4\Jobstreet\Business_Management_Combined.csv"
    merged_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    
    print(f"\n{'='*60}")
    print(f"🎉 MERGE COMPLETED!")
    print(f"{'='*60}")
    print(f"📁 Output file: Business_Management_Combined.csv")
    print(f"📊 Total rows: {len(merged_df)}")
    print(f"📋 Total files merged: {len(all_dataframes)}")
    
    # Tampilkan summary per file
    if 'Source_File' in merged_df.columns:
        print(f"\n📈 SUMMARY PER FILE:")
        file_counts = merged_df['Source_File'].value_counts().sort_index()
        for source_file, count in file_counts.items():
            print(f"  • {source_file}: {count} rows")
    
    # Tampilkan kolom yang tersedia
    print(f"\n📝 COLUMNS IN MERGED FILE:")
    for col in merged_df.columns:
        print(f"  • {col}")
    
    return output_path, len(merged_df)

if __name__ == "__main__":
    print("🚀 STARTING CSV MERGE PROCESS")
    print("📂 Target: Business & Management folder")
    print("🎯 Goal: Combine all CSV files into one")
    
    try:
        output_file, total_rows = merge_business_csv()
        print(f"\n✅ SUCCESS! Check the file: Business_Management_Combined.csv")
        print(f"📊 Contains {total_rows} total job links")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("💡 Make sure the Business & Management folder exists and contains CSV files")
