import streamlit as st
import pandas as pd
import duckdb

st.write("Hello world! Welcome to my first Streamlit app!")

data = {"a": [1, 2, 3], "b": [4, 5, 6]}
df = pd.DataFrame(data)

tab1, tab2, tab3, tab4 = st.tabs(["SQL Query", "Cat", "Dog", "Owl"])

with tab1:
    sql_query = st.text_area(label="Write your query:")
    result = duckdb.query(sql_query).df()
    st.write(f"Your query is: {sql_query}")
    st.dataframe(result)

with tab2:
    st.header("This is a cat.")
    st.image("https://static.streamlit.io/examples/cat.jpg", width=400)

with tab3:
    st.header("This is a dog.")
    st.image("https://static.streamlit.io/examples/dog.jpg", width=400)

with tab4:
    st.header("And this is an owl.")
    st.image("https://static.streamlit.io/examples/owl.jpg", width=400)
