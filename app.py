# pylint: disable=missing-module-docstring
import io

import duckdb
import pandas as pd
import streamlit as st

con = duckdb.connect(database="data/exercices_sql_tables.duckdb", read_only=False)

# Dataframe de résultat, prendre cette query et la mettre dans Duckdb SQL
# solution_df = duckdb.sql(ANSWER_STR).df()


with st.sidebar:
    theme = st.selectbox(
        "What would you like to review?",
        ["Cross-Joins", "GroupBy", "Windows Functions"],
        index=None,
        placeholder="Select a theme: ",
    )
    st.write("You selected:", theme)

    exercise = con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}'").df()
    st.write(exercise)

st.header("Enter your code: ")
query = st.text_area(label="Code SQL", key="user_input")
# if query:
#     result = duckdb.sql(query).df()
#     st.dataframe(result)
#
#     # Mettre les colonnes du DF result dans le même ordre que celle de la solution pour les comparer
#     # Try = prévision d'une KeyError en fonction de ce qu'à écrit l'utilisateur
#     try:
#         result = result[[solution_df.columns]]
#         # Comparer notre résultat  avec la solution avec compare
#         st.dataframe(result.compare(solution_df))
#     except KeyError as e:
#         st.write("Some columns are missing")
#
#     # Compare le nombre de lignes de différence avec shape
#     n_lines_difference = result.shape[0] - solution_df.shape[0]
#     if n_lines_difference != 0:
#         st.write(
#             f"Your result has a {n_lines_difference} lines difference with the solution"
#         )
#
# tab2, tab3 = st.tabs(["Tables", "Solution"])
#
# # Tables que l'utilisateur a à disposition
# with tab2:
#     st.write("table: beverages")
#     st.dataframe(beverages)
#     st.write("table: food_items")
#     st.dataframe(food_items)
#     st.write("expected:")
#     st.dataframe(solution_df)
#
# # Table à part avec la réponse, qui permet de chercher
# with tab3:
#     st.write(ANSWER_STR)
