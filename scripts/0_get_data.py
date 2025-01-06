import requests
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from utils import get_api_key, read_yaml


def get_page_data(
    api_key: str, 
    url: str,
    from_date: str, 
    to_date: str, 
    search_page: int = 1,
    n_results: int = 10,
) -> dict:
    """
    Query the API.
    """
    params = {
        "api-key": api_key,
        "section": "food",
        "q": "recipe",
        "from-date": from_date,
        "to-date": to_date,
        "page": search_page,
        "page-size": n_results,
        "show-fields": "byline,headline,trailText,thumbnail,bodyText,publication,productionOffice",
        "show-tags": "keyword",
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def get_recipes_from_page(
        api_key: str, 
        url: str, 
        from_date: str, 
        to_date: str, 
        page: int
    ) -> list:
    """
    Process data from one page of API results.
    """
    data = get_page_data(api_key, url, from_date, to_date, page)
    results = data["response"]["results"]
    recipes = []

    for r in results:
        if 'recipe' not in r.get("webTitle", "").lower():
            continue

        fields = r["fields"]
        tags = [t["webTitle"] for t in r["tags"]]
        webtitle_sections = r["webTitle"].split("|")
        title = webtitle_sections[0].strip()
        section = (
            None if len(webtitle_sections) <= 1 
            else webtitle_sections[1].strip()
        )

        article = dict(
            title=title,
            section=section,
            published_at=r.get("webPublicationDate"),
            summary=fields.get("trailText"),
            author=fields.get("byline"),
            publication=fields.get("publication"),
            production_office=fields.get("productionOffice"),
            url=r.get("webUrl"),
            thumbnail_url=fields.get("thumbnail"),
            body=fields.get("bodyText"),
            tags=tags,
        )
        recipes.append(article)
    
    return recipes


def get_recipes(
    api_key: str,
    url: str,
    from_date: str,
    to_date: str,
) -> pd.DataFrame:
    """
    Get all recipes from the API.
    """
    total_pages = get_page_data(api_key, url, from_date, to_date, 1)["response"]["pages"]

    recipes = []
    tasks = range(1, total_pages + 1)

    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(
                get_recipes_from_page, 
                api_key, url, from_date, to_date, page)
            for page in tasks
        ]

        for future in tqdm(
            as_completed(futures), 
            total=len(futures), 
            desc="Fetching recipes..."
        ): 
            recipes.extend(future.result())
    
    return pd.DataFrame(recipes)


def main() -> None:
    # read config
    config = read_yaml("config/data_config.yaml")
    source_name = config["source_name"]
    api_key = get_api_key(config["api_key_name"])
    base_url = config["base_url"]
    n_days = config["n_days_fill"]
    output_folder = Path(config["output_folder"])
    output_file = Path(config["output_file"] + '_raw.csv')

    # get date range
    today = datetime.now()
    from_date = (
        today - timedelta(days=n_days)
    ).strftime("%Y-%m-%d")
    to_date = today.strftime("%Y-%m-%d")

    print(f"Updating the recipe database with articles from {source_name}.")
    print(f"Fetching articles from {from_date} to {to_date}...")

    df = get_recipes(api_key, base_url, from_date, to_date)

    output_folder.mkdir(parents=True, exist_ok=True)
    output_path = output_folder / output_file

    df.to_csv(output_path, index=False)
    print(f"Saved {len(df)} recipes to {output_path}.")


if __name__ == "__main__":
    main()