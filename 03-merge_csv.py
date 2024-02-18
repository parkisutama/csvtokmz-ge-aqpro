import pandas as pd

# Read the CSV files
df1 = pd.read_csv('C:/Github\Belajar QGIS dan Alpine Quest/test_2024-02-18/source_2.csv')
df2 = pd.read_csv('C:/Github\Belajar QGIS dan Alpine Quest/test_2024-02-18/file_list.csv')

# Merge the files based on "KODE POHON" column
merged_df = pd.merge(df1, df2, on='KODE POHON')

# Save the merged data to a new CSV file
merged_df.to_csv('sourcemap.csv', index=False)