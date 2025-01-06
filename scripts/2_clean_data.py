import pandas as pd
from pathlib import Path
from utils import read_yaml

def main() -> None:
    config = read_yaml("config/data_config.yaml")
    data_folder = Path(config["output_folder"])
    input_file = Path(config["output_file"] + '.csv')
    output_file = Path(config["output_file"] + '_clean.csv')
    
    print(f"Cleaning data from {data_folder / input_file}...")
    df = pd.read_csv(data_folder / input_file)
    df.fillna('', inplace=True)
    cols = df.columns
    df['id'] = df.index
    df = df[['id'] + list(cols)]
    df['section'] = (
        df['section']
        .str.replace("Masterclasss", "Masterclass")
        .str.replace("cook the perfect", "make the perfect")
        .str.lower()
        .map(lambda x: 'how to make the perfect ...' if 'make the perfect' in x else x)
    )

    output_path = data_folder / output_file
    df.to_csv(output_path, index=False)
    print(f"Saved {len(df)} recipes to {output_path}.")

if __name__ == "__main__":
    main()