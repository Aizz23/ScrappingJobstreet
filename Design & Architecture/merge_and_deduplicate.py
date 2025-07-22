import pandas as pd
import os
import glob

def merge_design_architecture_csv():
    """Menggabungkan semua file CSV di folder Design & Architecture menjadi satu file dan hapus duplikat"""
    
    # Path ke folder Design & Architecture
    design_folder = r"c:\Users\DEMO PAMERAN\Downloads\Semester 4\Jobstreet\Design & Architecture"
    
    # Cari semua file CSV di folder (kecuali file yang sudah merged)
    csv_files = glob.glob(os.path.join(design_folder, "*.csv"))
    
    # Filter out files yang sudah merupakan hasil merge
    csv_files = [f for f in csv_files if not any(exclude in os.path.basename(f).lower() 
                                                for exclude in ['combined', 'merged', 'no_duplicate', 'backup'])]
    
    print(f"🔍 Found {len(csv_files)} CSV files in Design & Architecture folder:")
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
    print(f"📊 Initial combined data: {len(merged_df)} rows")
    
    # Hapus duplikat berdasarkan Link
    initial_count = len(merged_df)
    if 'Link' in merged_df.columns:
        print(f"\n🔍 Checking for duplicate links...")
        duplicates_count = merged_df.duplicated(subset=['Link']).sum()
        print(f"🔗 Duplicate links found: {duplicates_count}")
        
        merged_df = merged_df.drop_duplicates(subset=['Link'], keep='first')
        final_count = len(merged_df)
        print(f"🗑️  Removed {initial_count - final_count} duplicate links")
    else:
        print("⚠️  'Link' column not found, skipping duplicate removal")
        final_count = len(merged_df)
    
    # Urutkan berdasarkan keyword atau source file
    if 'Keyword' in merged_df.columns:
        merged_df = merged_df.sort_values(['Keyword', 'Source_File'])
    else:
        merged_df = merged_df.sort_values('Source_File')
    
    # Reset index
    merged_df = merged_df.reset_index(drop=True)
    
    # Simpan hasil gabungan
    output_path = os.path.join(design_folder, "Design_Architecture_Combined_NoDuplicates.csv")
    merged_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    
    print(f"\n{'='*70}")
    print(f"🎉 MERGE & DEDUPLICATION COMPLETED!")
    print(f"{'='*70}")
    print(f"📁 Output file: Design_Architecture_Combined_NoDuplicates.csv")
    print(f"📊 Final rows: {len(merged_df)}")
    print(f"📋 Files merged: {len(all_dataframes)}")
    print(f"🗑️  Duplicates removed: {initial_count - final_count}")
    
    # Tampilkan summary per file
    if 'Source_File' in merged_df.columns:
        print(f"\n📈 SUMMARY PER SOURCE FILE:")
        file_counts = merged_df['Source_File'].value_counts().sort_index()
        for source_file, count in file_counts.items():
            print(f"  • {source_file}: {count} unique links")
    
    # Tampilkan summary per keyword
    if 'Keyword' in merged_df.columns:
        print(f"\n📋 SUMMARY PER KEYWORD:")
        keyword_counts = merged_df['Keyword'].value_counts().sort_index()
        for keyword, count in keyword_counts.items():
            print(f"  • {keyword}: {count} links")
        print(f"  📊 Total unique keywords: {len(keyword_counts)}")
    
    # Tampilkan kolom yang tersedia
    print(f"\n📝 COLUMNS IN FINAL FILE:")
    for col in merged_df.columns:
        print(f"  • {col}")
    
    return output_path, len(merged_df)

if __name__ == "__main__":
    print("🚀 STARTING DESIGN & ARCHITECTURE CSV MERGE & DEDUPLICATION")
    print("📂 Target: Design & Architecture folder")
    print("🎯 Goal: Combine all CSV files + Remove duplicates")
    
    try:
        output_file, total_rows = merge_design_architecture_csv()
        print(f"\n✅ SUCCESS! Check the file: Design_Architecture_Combined_NoDuplicates.csv")
        print(f"📊 Contains {total_rows} unique job links")
        print(f"💡 No duplicates, ready to use!")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("💡 Make sure the Design & Architecture folder exists and contains CSV files")
