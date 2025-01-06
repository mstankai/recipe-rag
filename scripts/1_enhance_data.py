import pandas as pd
from pathlib import Path
from tqdm import tqdm
from transformers import pipeline
from utils import read_yaml


def get_details(body: str) -> str:
    """
    Find the prep time, cook time, and serving size.
    """
    prep_time, cook_time, serving_size = None, None, None
    prep, cook, serves = ( s in body for s in [" Prep ", " Cook ", " Serves "] )
    if prep and cook:
        prep_time = "Prep " + body.split("Prep ")[1].split(" Cook")[0]
    if cook and serves:
        cook_time = "Cook " + body.split("Cook ")[1].split(" Serves")[0]
    if serves:
        serving_size = body.split("Serves ")[1].split(" ")[0]
    return prep_time, cook_time, serving_size

def clasify_column(
        input_col: pd.Series, 
        model:str, 
        classes: list[str],
        batch_size: int = 16
        ) -> list[str]:
    """
    Classify a column of text using a zero-shot classifier.
    """
    classifier = pipeline("zero-shot-classification", model=model)
    n_rows = len(input_col)
    labels = []
    texts = input_col.to_list()
    print(f"\nPredicting labels using {model}...")
    print(f"Classes: {classes}\n")
    for i in tqdm(range(0, n_rows, batch_size)):
        batch = texts[i : i + batch_size]
        results = classifier(batch, classes, multi_label=False)
        labels += [result["labels"][0] for result in results]

    return labels

def main() -> None:
    config = read_yaml("config/data_config.yaml")
    data_folder = Path(config["output_folder"])
    input_file = Path(config["output_file"] + '_raw.csv')
    output_file = Path(config["output_file"] + '.csv')
    model = config["enhancement_model"]
    cuisines = config["cuisines"]

    df = pd.read_csv(data_folder / input_file)

    print(f"Enhancing {len(df)} rows of data from {input_file}")
    
    df[['prep_time', 'cook_time', 'serving_size']] = df['body'].apply(get_details).apply(pd.Series)
    df['short_context'] = (
        df['title'] 
        + ' ' + df['section'].fillna('')
        + ': ' + df['summary'] 
        + ' TAGS: ' + df['tags'] 
    )
    df['cuisine'] = clasify_column(df['short_context'], model, cuisines)
    df.drop(columns=['short_context'], inplace=True)
    output_path = data_folder / output_file
    df.to_csv(output_path, index=False)
    print(f"Saved {len(df)} recipes to {output_path}.")

if __name__ == "__main__":
    main()