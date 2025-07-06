import pandas as pd

def combine_excel_files(filenames, output_filename):
    dfs = []
    for f in filenames:
        try:
            df = pd.read_excel(f, engine="openpyxl")
            dfs.append(df)
            print(f"Successfully read {f}")
        except Exception as e:
            print(f"Error reading {f}: {str(e)}")
    
    if dfs:
        combined_df = pd.concat(dfs, ignore_index=True)
        combined_df.to_excel(output_filename, index=False, engine="openpyxl")
        print(f"Files combined and saved as '{output_filename}'")
    else:
        print("No valid files to combine")