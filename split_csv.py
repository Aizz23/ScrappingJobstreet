import pandas as pd
import os
import math

def split_csv_into_4_files():
    """
    Membagi file ALL_SCRAPED_JOBSTREET_COMBINED.csv menjadi 4 file yang lebih kecil
    """
    
    # Path file input
    base_dir = r"c:\Users\DEMO PAMERAN\Downloads\Semester 4\Jobstreet"
    input_file = os.path.join(base_dir, "ALL_SCRAPED_JOBSTREET_COMBINED.csv")
    
    print("🔪 SPLITTING CSV FILE INTO 4 PARTS")
    print("="*60)
    print(f"📂 Base directory: {base_dir}")
    print(f"📄 Input file: ALL_SCRAPED_JOBSTREET_COMBINED.csv")
    
    # Cek apakah file ada
    if not os.path.exists(input_file):
        print(f"❌ File tidak ditemukan: {input_file}")
        return
    
    print(f"\n📖 Reading CSV file...")
    try:
        # Baca file CSV
        df = pd.read_csv(input_file)
        total_rows = len(df)
        print(f"✅ File loaded successfully!")
        print(f"📊 Total rows: {total_rows:,}")
        print(f"📋 Columns: {list(df.columns)}")
        
        # Hitung ukuran setiap chunk
        chunk_size = math.ceil(total_rows / 4)
        print(f"🔢 Rows per file: ~{chunk_size:,}")
        
        # Split dan simpan 4 file
        for i in range(4):
            start_idx = i * chunk_size
            end_idx = min((i + 1) * chunk_size, total_rows)
            
            # Ambil subset data
            chunk_df = df.iloc[start_idx:end_idx].copy()
            
            # Reset index
            chunk_df = chunk_df.reset_index(drop=True)
            
            # Nama file output
            output_filename = f"ALL_SCRAPED_JOBSTREET_PART_{i+1}_of_4.csv"
            output_path = os.path.join(base_dir, output_filename)
            
            # Simpan file
            chunk_df.to_csv(output_path, index=False, encoding='utf-8-sig')
            
            print(f"\n📄 Part {i+1}/4 created:")
            print(f"  • File: {output_filename}")
            print(f"  • Rows: {len(chunk_df):,} (index {start_idx:,} to {end_idx-1:,})")
            print(f"  • Size: ~{len(chunk_df) * 0.5 / 1000:.1f} KB")
            
            # Tampilkan sample data jika ada kolom Category
            if 'Category' in chunk_df.columns:
                category_counts = chunk_df['Category'].value_counts()
                print(f"  • Categories: {len(category_counts)} unique")
                print(f"  • Top 3 categories: {list(category_counts.head(3).index)}")
        
        print(f"\n{'='*60}")
        print(f"🎉 SPLIT COMPLETED!")
        print(f"{'='*60}")
        print(f"📊 Original file: {total_rows:,} rows")
        print(f"📁 Split into: 4 files")
        print(f"📄 Files created:")
        for i in range(4):
            print(f"  • ALL_SCRAPED_JOBSTREET_PART_{i+1}_of_4.csv")
        
        print(f"\n💡 TIPS:")
        print(f"  • Each file contains ~{chunk_size:,} rows")
        print(f"  • Files are ready for processing")
        print(f"  • Original file remains unchanged")
        print(f"  • Use these for parallel processing or easier handling")
        
        return True
        
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False

def split_by_category():
    """
    Alternative: Split berdasarkan kategori (jika ingin split yang lebih logis)
    """
    
    base_dir = r"c:\Users\DEMO PAMERAN\Downloads\Semester 4\Jobstreet"
    input_file = os.path.join(base_dir, "ALL_SCRAPED_JOBSTREET_COMBINED.csv")
    
    print("\n🔄 ALTERNATIVE: Split by Category")
    print("="*50)
    
    try:
        df = pd.read_csv(input_file)
        
        if 'Category' not in df.columns:
            print("❌ No 'Category' column found")
            return False
        
        categories = df['Category'].unique()
        print(f"📊 Found {len(categories)} categories:")
        
        category_counts = df['Category'].value_counts()
        for cat, count in category_counts.items():
            print(f"  • {cat}: {count:,} rows")
        
        # Group categories into 4 roughly equal groups
        categories_sorted = category_counts.sort_values(ascending=False)
        
        # Distribute categories into 4 groups trying to balance row counts
        groups = [[] for _ in range(4)]
        group_sizes = [0] * 4
        
        for category, count in categories_sorted.items():
            # Find group with smallest current size
            min_group_idx = group_sizes.index(min(group_sizes))
            groups[min_group_idx].append(category)
            group_sizes[min_group_idx] += count
        
        print(f"\n📋 Category distribution:")
        for i, group in enumerate(groups):
            if group:  # Only show non-empty groups
                group_df = df[df['Category'].isin(group)]
                output_filename = f"ALL_SCRAPED_JOBSTREET_CATEGORIES_GROUP_{i+1}.csv"
                output_path = os.path.join(base_dir, output_filename)
                
                group_df.to_csv(output_path, index=False, encoding='utf-8-sig')
                
                print(f"  Group {i+1}: {len(group_df):,} rows")
                print(f"    Categories: {', '.join(group)}")
                print(f"    File: {output_filename}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in category split: {e}")
        return False

if __name__ == "__main__":
    print("🚀 CSV SPLITTER")
    print("Choose splitting method:")
    print("1. Split into 4 equal parts (by rows)")
    print("2. Split by categories into 4 groups")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        split_csv_into_4_files()
    elif choice == "2":
        split_by_category()
    else:
        print("Invalid choice. Running default split by rows...")
        split_csv_into_4_files()
