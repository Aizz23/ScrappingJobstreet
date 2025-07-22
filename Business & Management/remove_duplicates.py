import pandas as pd
import os

# Path ke file CombinedAll.csv
file_path = r"c:\Users\DEMO PAMERAN\Downloads\Semester 4\Jobstreet\Business & Management\CombinedAll.csv"

print("🔍 REMOVING DUPLICATES FROM COMBINED FILE")
print("="*50)

# Baca file CSV
try:
    df = pd.read_csv(file_path)
    print(f"📊 Original data: {len(df)} rows")
    
    # Tampilkan kolom yang tersedia
    print(f"📋 Columns: {list(df.columns)}")
    
    # Cek duplikat berdasarkan kolom Link
    if 'Link' in df.columns:
        duplicates_count = df.duplicated(subset=['Link']).sum()
        print(f"🔗 Duplicate links found: {duplicates_count}")
        
        # Hapus duplikat berdasarkan Link, keep='first' (simpan yang pertama)
        df_cleaned = df.drop_duplicates(subset=['Link'], keep='first')
        print(f"✅ After removing duplicates: {len(df_cleaned)} rows")
        print(f"🗑️  Removed: {len(df) - len(df_cleaned)} duplicate rows")
        
        # Simpan file yang sudah dibersihkan
        output_file = "CombinedAll_NoDuplicates.csv"
        df_cleaned.to_csv(output_file, index=False)
        print(f"💾 Clean data saved to: {output_file}")
        
        # Tampilkan statistik per keyword
        if 'Keyword' in df_cleaned.columns:
            print(f"\n📊 BREAKDOWN BY KEYWORD:")
            keyword_stats = df_cleaned['Keyword'].value_counts()
            for keyword, count in keyword_stats.items():
                print(f"  • {keyword}: {count} links")
            print(f"  📊 Total unique keywords: {len(keyword_stats)}")
        
        # Overwrite file asli jika user mau
        replace_original = input(f"\n Replace original file '{file_path}' with clean version? (y/n): ").lower()
        if replace_original == 'y':
            df_cleaned.to_csv(file_path, index=False)
            print(f"✅ Original file '{file_path}' has been updated (duplicates removed)")
            # Hapus file temporary
            if os.path.exists(output_file):
                os.remove(output_file)
                print(f"🗑️  Temporary file '{output_file}' removed")
        else:
            print(f"ℹ️  Original file kept unchanged. Clean version saved as '{output_file}'")
            
    else:
        print("❌ Column 'Link' not found. Available columns:", list(df.columns))
        
except FileNotFoundError:
    print(f"❌ File '{file_path}' not found!")
except Exception as e:
    print(f"❌ Error: {e}")

print(f"\n DUPLICATE REMOVAL COMPLETED!")
