import pandas as pd
from ast import literal_eval
from pathlib import Path
from utils import read_yaml


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df.fillna('', inplace=True)
    cols = df.columns
    df['id'] = df.index
    df = df[['id'] + list(cols)]
    return df

def clean_section_column(df: pd.DataFrame) -> pd.DataFrame:
    df['section'] = (
        df['section']
        .str.replace("Masterclasss", "Masterclass")
        .str.replace("cook the perfect", "make the perfect")
        .str.lower()
        .map(lambda x: 'how to make the perfect ...' if 'make the perfect' in x else x)
    )
    return df

def prep_data(df: pd.DataFrame) -> pd.DataFrame:
    df['tag_str'] = df.tags.map(lambda x: ', '.join(literal_eval(x)) )
    df['content'] = (
        'Title: ' + df['title'] + ' | '
        + df['section'] + ' '
        + 'Author: ' + df['author'] + ' '
        + 'Text:  ' + df['body'] + ' '
        + '. KEYWORDS: ' + df['tag_str']  
    )
    return df


def main() -> None:
    config = read_yaml("config/data_config.yaml")
    data_folder = Path(config["output_folder"])
    input_file = Path(config["output_file"] + '.csv')
    output_file = Path(config["output_file"] + '_rag_input.csv')
    
    print(f"Preparing data for embedding")
    print(f"Reading data from {data_folder / input_file} ...")
    
    df = pd.read_csv(data_folder / input_file)
    
    df = clean_data(df)
    df = clean_section_column(df)
    df = prep_data(df)

    output_path = data_folder / output_file
    df.to_csv(output_path, index=False)
    print(f"Saved {len(df)} data to {output_path}.")

if __name__ == "__main__":
    main()