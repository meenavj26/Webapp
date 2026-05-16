import requests
from bs4 import BeautifulSoup
import json
import time

URLS = [
    "https://www.bbcgoodfood.com/recipes/chicken-pasta-bake",
    "https://www.bbcgoodfood.com/recipes/creamy-mushroom-pasta",
]

headers = {
    "User-Agent": "Mozilla/5.0"
}


def extract_recipe(soup):
    scripts = soup.find_all("script", type="application/ld+json")

    for script in scripts:
        try:
            if not script.string:
                continue

            data = json.loads(script.string)

            if isinstance(data, dict) and data.get("@type") == "Recipe":
                return data["name"], data["recipeIngredient"]

            if isinstance(data, dict) and "@graph" in data:
                for item in data["@graph"]:
                    if item.get("@type") == "Recipe":
                        return item["name"], item["recipeIngredient"]

        except:
            continue

    return None, []


recipes = []

for url in URLS:
    print("Scraping:", url)

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    title, ingredients = extract_recipe(soup)

    print("TITLE:", title)
    print("ING COUNT:", len(ingredients))

    if title and ingredients:
        recipes.append({
            "title": title,
            "ingredients": ingredients,
            "last_updated": time.strftime("%Y-%m-%d %H:%M:%S")
        })

    time.sleep(1)

with open("recipes.json", "w", encoding="utf-8") as f:
    json.dump(recipes, f, indent=4)

print("DONE!")