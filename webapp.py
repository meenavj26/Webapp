import streamlit as st
import json

st.title("BBC Good Food Recipe App")


with open("recipes.json", "r") as f:
    recipes = json.load(f)

if not recipes:
    st.error("No data found. Run scrape.py first.")
    st.stop()

st.caption(f"Last updated: {recipes[0]['last_updated']}")

for recipe in recipes:
    st.header(recipe["title"])

    for item in recipe["ingredients"]:
        st.write("- " + item)

    st.write("---")