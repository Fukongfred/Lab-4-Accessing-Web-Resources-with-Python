import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os

from db import Database

load_dotenv()

def fetch_books(query, filter_by, order_by):
    with Database(os.getenv('DATABASE_URL')) as db:
        query = f"""
        SELECT * FROM books
        WHERE name ILIKE '%{query}%' OR description ILIKE '%{query}%'
        ORDER BY {filter_by} {order_by}
        """
        return pd.read_sql(query, db.connection)

st.title('eBookstore Search&Filter')

query = st.text_input("Search by book name or description", "")

filter_option = st.selectbox(
    "Filter by:",
    options=['rating', 'price'],
    index=0
)

order_option = st.selectbox(
    "Order:",
    options=['ASC', 'DESC'],
    index=0
)

if st.button("Search"):
    books_df = fetch_books(query, filter_option, order_option)
    st.dataframe(books_df)
else:
    st.write("Enter a search query and press 'Search'.")