# pylint: disable=missing-module-docstring

import os
import logging
import duckdb
import streamlit as st
from datetime import date, timedelta


if "data" not in os.listdir():
    logging.error(os.listdir())
    logging.error("creating folder data")
    os.mkdir("data")

if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read())
    # subprocess.run(["python", "init_db.py"]) > mieux mais ne marche pas tres bien sur Streamlit

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)


def check_users_solution(user_query: str) -> None:
    """
    Checks that user SQL query is correct by:
    1: checking the columns
    2: checking the values
    :param user_query: a string containing the query inserted by the user
    """
    result = con.execute(user_query).df()
    st.dataframe(result)
    # Mettre les colonnes du DF result dans le même ordre que celle de la solution pour les comparer
    # Try = prévision d'une KeyError en fonction de ce qu'à écrit l'utilisateur
    try:
        result = result[solution_df.columns]
        # Comparer notre résultat avec la solution avec compare
        st.dataframe(result.compare(solution_df))
        if result.compare(solution_df).shape == (0, 0):
            st.write("Correct !")
            st.balloons()
    except KeyError as e:
        st.write("Some columns are missing!")
    # Compare le nombre de lignes de différence avec shape
    n_lines_difference = result.shape[0] - solution_df.shape[0]
    if n_lines_difference != 0:
        st.write(
            f"Your result has a {n_lines_difference} lines difference with the solution_df"
        )


with st.sidebar:
    available_themes_df = con.execute("SELECT DISTINCT theme FROM memory_state").df()
    # st.dataframe(available_themes_df["theme"].unique())
    # st.write(available_themes_df["theme"].unique())
    theme = st.selectbox(
        "What would you like to review?",
        available_themes_df["theme"].unique(),
        index=None,
        placeholder="Select a theme:",
    )
    if theme:
        st.write(f"You selected this {theme}:")
        select_exercise_query = f"SELECT * FROM memory_state WHERE theme = '{theme}'"
    else:
        select_exercise_query = f"SELECT * FROM memory_state"
    exercise = (
        con.execute(select_exercise_query)
        .df()
        .sort_values("last_reviewed")
        .reset_index(drop=True)
    )
    st.write(exercise)

    exercise_name = exercise.loc[0, "exercise_name"]
    with open(f"answers/{exercise_name}.sql", "r") as f:
        answer = f.read()

    solution_df = con.execute(answer).df()

st.header("Enter your code: ")
query = st.text_area(label="Enter your code SQL here:", key="user_input")

if query:
    check_users_solution(query)

for n_days in [2, 7, 21]:
    if st.button(f"Review in {n_days} days"):
        next_review = date.today() + timedelta(days=n_days)
        con.execute(
            f"UPDATE memory_state SET last_reviewed = '{next_review}' WHERE exercise_name = '{exercise_name}'"
        )
        st.rerun()

if st.button("Reset"):
    con.execute(f"UPDATE memory_state SET last_reviewed = '1970-01-01'")
    st.rerun()

tab2, tab3 = st.tabs(["Tables", "Solution"])
# Tables que l'utilisateur a à disposition
with tab2:
    exercise_tables = exercise.loc[0, "tables"]
    for table in exercise_tables:
        st.write(f"table: {table}")
        df_table = con.execute(f"SELECT * FROM {table}").df()
        st.dataframe(df_table)

# Table à part avec la réponse, qui permet de chercher
with tab3:
    st.write(answer)
