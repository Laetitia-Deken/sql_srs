# pylint: disable=missing-module-docstring

import os
import logging
import duckdb
import streamlit as st
from datetime import date, timedelta

if "data" not in os.listdir():
    print("creating folder data")
    logging.error(os.listdir())
    logging.error("creating folder data")
    os.mkdir("data")

if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read())
    # subprocess.run(["python", "init_db.py"])

con = duckdb.connect(database="data/exercices_sql_tables.duckdb", read_only=False)


with st.sidebar:
    theme = st.selectbox(
        "What would you like to review?",
        ["cross_joins", "GroupBy", "window_functions"],
        index=None,
        placeholder="Select a theme: ",
    )
    st.write("You selected:", theme)

    exercise = con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}'").df().sort_values("last_reviewed").reset_index()
    st.write(exercise)

    if not exercise.empty:
        exercise_name = exercise.loc[0, "exercise_name"]
    else:
        # Gérer le cas où le DataFrame est vide
        print("Le DataFrame 'exercise' est vide.")
        
    with open(f"answers/{exercise_name}.sql", "r") as f:
        answer = f.read()

import io

import duckdb
import pandas as pd
import streamlit as st

CSV = """
beverage,price
orange juice,2.5
Expresso,2
Tea,3
"""
beverages = pd.read_csv(io.StringIO(CSV))

# Création de la donnée
CSV2 = """
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
"""
# Pandas dataframe
food_items = pd.read_csv(io.StringIO(CSV2))

# Ecriture de la réponse attendue par l'utilisateur pour que cela fonctionne
ANSWER_STR = """
SELECT * FROM beverages
CROSS JOIN food_items
"""

# Dataframe de résultat, prendre cette query et la mettre dans Duckdb SQL
solution_df = duckdb.sql(ANSWER_STR).df()


with st.sidebar:
    option = st.selectbox(
        "What would you like to review?",
        ["Joins", "GroupBy", "Windows Functions"],
        index=None,
        placeholder="Select a theme: ",
    )
    st.write("You selected:", option)

    exercise = con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}'").df().sort_values("last_reviewed").reset_index()
    st.write(exercise)

    if not exercise.empty:
        exercise_name = exercise.loc[0, "exercise_name"]
    else:  # Gérer le cas où le DataFrame est vide
        print("Le DataFrame 'exercise' est vide.")
        
    with open(f"answers/{exercise_name}.sql", "r") as f:
        answer = f.read()

    # Dataframe de résultat, prendre cette query et la mettre dans Duckdb SQL
    solution_df = con.execute(answer).df()


st.header("Enter your code: ")
query = st.text_area(label="Code SQL", key="user_input")
if query:
    result = duckdb.sql(query).df()
    st.dataframe(result)

    # Mettre les colonnes du DF result dans le même ordre que celle de la solution pour les comparer
    # Try = prévision d'une KeyError en fonction de ce qu'a écrit l'utilisateur
    try:
        result = result[[solution_df.columns]]
        # Comparer notre résultat  avec la solution avec compare
        st.dataframe(result.compare(solution_df))
    except KeyError as e:
        st.write("Some columns are missing")

    # Compare le nombre de lignes de différence avec shape
    n_lines_difference = result.shape[0] - solution_df.shape[0]
    if n_lines_difference != 0:
        st.write(
            f"Your result has a {n_lines_difference} lines difference with the solution"
        )

tab2, tab3 = st.tabs(["Tables", "Solution"])

# Tables que l'utilisateur a à disposition
with tab2:
    st.write("table: beverages")
    st.dataframe(beverages)
    st.write("table: food_items")
    st.dataframe(food_items)
    st.write("expected:")
    st.dataframe(solution_df)

# Table à part avec la réponse, qui permet de chercher
with tab3:
    st.write(ANSWER_STR)
