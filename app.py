import streamlit as st
import pandas as pd
import duckdb
import io

csv = """
beverage,price
orange juice,2.5
Expresso,2
Tea,3
"""
beverages = pd.read_csv(io.StringIO(csv))

# Création de la donnée
csv2 = """
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
"""
# Pandas dataframe
food_items = pd.read_csv(io.StringIO(csv2))

# Ecriture de la réponse attendue par l'utilisateur pour que cela fonctionne
answer = """
SELECT * FROM beverages
CROSS JOIN food_items
"""

# Dataframe de résultat, prendre cette query et la mettre dans Duckdb SQL
solution = duckdb.sql(answer).df()


with st.sidebar:
    option = st.selectbox(
       "What would you like to review?",
       ["Joins", "GroupBy", "Windows Functions"],
       index=None,
       placeholder="Select a theme: ",
    )
    st.write('You selected:', option)


st.header("Enter your code: ")
query = st.text_area(label="Code SQL", key="user_input")
if query:
    result = duckdb.sql(query).df()
    st.dataframe(result)

tab2, tab3 = st.tabs(["Tables", "Solution"])

# Tables que l'utilisateur a à disposition
with tab2:
    st.write("table: beverages")
    st.dataframe(beverages)
    st.write("table: food_items")
    st.dataframe(food_items)
    st.write("expected:")
    st.dataframe(solution)

# Table à part avec la réponse, qui permt de chacher
with tab3:
    st.write(answer)
