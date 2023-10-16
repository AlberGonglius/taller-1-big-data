import streamlit as st
from PIL import Image
import pandas as pd
import altair as alt
from streamlit_card import card


# ========== Loading Data ============

title_count_df_part_1=pd.read_parquet("data/news/title_count/part-00000.parquet")
title_count_df_part_2 = pd.read_parquet("data/news/title_count/part-00001.parquet")
title_count_df = pd.concat([title_count_df_part_1, title_count_df_part_2])
title_count_df = title_count_df.tail(-1) # Removing first word
content_count_df=pd.read_parquet("data/news/text_count/part-00000.parquet")
content_count_df = content_count_df.tail(-1) # Removing first word

# ========== HEADER ============
st.header("Análisis de Noticias en español del 2016")



# Metrics
col1, col2, col3 = st.columns(3)
col1.metric(label="Noticias en 2016", value=341696, delta=2016)
col2.metric(label="Palabras analizadas", value=len(title_count_df), delta=-1000)
col3.metric(label="Palabra más frecuente", value=10706, delta=1)

# Images
image = Image.open('assets/news.jpg')
st.image(image, width=600)

# ========== TABS ============

tab1, tab2 = st.tabs(["📈 Títulos", "🗃 Contenido"])
# Tab 1: Titles
top_10_title_df = title_count_df[:10]
tab1.subheader("Top 10 palabras más frecuentes")
# Chart
bars = alt.Chart(top_10_title_df).mark_bar().encode(
        x="count",
        y=alt.Y("word", sort=alt.EncodingSortField(field="count", order="descending"))
)

text = alt.Chart(top_10_title_df).mark_text(color="white").encode(
    y=alt.Y('word', axis=None, sort=alt.EncodingSortField(field="count", order="descending")),
    text=alt.Text('count')
).properties(width=30)

chart = bars | text

tab1.altair_chart(chart, use_container_width=True)

with tab1:
    # Table
    st.subheader("Listado total de palabras")
    st.dataframe(title_count_df[:100], height=400, use_container_width=True)
    st.subheader("Trending Topics")
    col1, col2 = st.columns(2)
    # Images
    with col1:
        cards_col1= [
            {"title": "1. Diesel", "text": "10.706", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Red_diesel_tank.jpg/220px-Red_diesel_tank.jpg"},
            {"title": "12. PSOE", "text": "5.187", "image": "https://s1.eestatic.com/2023/10/09/espana/politica/800680267_236676146_1706x960.jpg"},
            {"title": "15. Trump", "text": "4.257", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Donald_Trump_official_portrait.jpg/800px-Donald_Trump_official_portrait.jpg"},
            {"title": "21. Rajoy", "text": "3.532", "image": "https://upload.wikimedia.org/wikipedia/commons/d/d7/Mariano_Rajoy_in_2018.jpg"}
        ]
        for card_element in cards_col1:
            card(
                title=card_element["title"],
                text=card_element["text"],
                image=card_element["image"],
                key=card_element["title"],
                on_click=lambda: print("Clicked!"),
                styles={
                    "card": {
                        "margin": "0",
                    }}
            )
    with col2:
        cards_col1= [
            {"title": "2. Madrid", "text": "9.201", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Torres_de_Madrid_%28detalle%29.JPG/1280px-Torres_de_Madrid_%28detalle%29.JPG"},
            {"title": "11. 4x4", "text": "5.485", "image": "https://www.motor.com.co/__export/1666113317433/sites/motor/img/2022/10/18/jeep-avenger-4x4-concept-00002_1.jpg_242310155.jpg"},
            {"title": "16. Octubre", "text": "4.202", "image": "https://phantom-marca.unidadeditorial.es/c7bbc664ee81008358e697d88d95ad3e/resize/828/f/jpg/assets/multimedia/imagenes/2022/10/30/16671534236650.jpg"},
            {"title": "33. EEUU", "text": "2.845", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Flag_of_the_United_States.svg/800px-Flag_of_the_United_States.svg.png"},
        ]
        for card_element in cards_col1:
            card(
                title=card_element["title"],
                text=card_element["text"],
                image=card_element["image"],
                key=card_element["title"],
                on_click=lambda: print("Clicked!"),
                styles={
                    "card": {
                        "margin": "0",
                    }}
            )


# Tab 2: Content
tab2.subheader("Top 10 palabras más frecuentes")

# Chart
bars = alt.Chart(content_count_df[:10]).mark_bar().encode(
        x="count",
        y=alt.Y("word", sort=alt.EncodingSortField(field="count", order="descending"))
)

text = alt.Chart(content_count_df[:10]).mark_text(color="white").encode(
    y=alt.Y('word', axis=None, sort=alt.EncodingSortField(field="count", order="descending")),
    text=alt.Text('count')
).properties(width=30)

chart = bars | text

tab2.altair_chart(chart, use_container_width=True)

with tab2:
    # Table
    st.subheader("Listado total de palabras")
    st.dataframe(content_count_df[:99], height=400, use_container_width=True)
    st.subheader("Palabras interesantes")
    col3, col4 = st.columns(2)
    # Images
    with col3:
        cards_col1= [
            {"title": "4. Octubre", "text": "10.706", "image": "https://phantom-marca.unidadeditorial.es/c7bbc664ee81008358e697d88d95ad3e/resize/828/f/jpg/assets/multimedia/imagenes/2022/10/30/16671534236650.jpg"},
            {"title": "15. Presidente", "text": "5.187", "image": "https://upload.wikimedia.org/wikipedia/commons/d/d7/Mariano_Rajoy_in_2018.jpg"},
        ]
        for card_element in cards_col1:
            card(
                title=card_element["title"],
                text=card_element["text"],
                image=card_element["image"],
                key=card_element["title"],
                on_click=lambda: print("Clicked!"),
                styles={
                    "card": {
                        "margin": "0",
                    }}
            )
    with col4:
        cards_col1= [
            {"title": "9. Gobierno", "text": "9.201", "image": "https://concepto.de/wp-content/uploads/2015/03/gobierno-1-e1549740896200.jpg"},
            {"title": "18. País", "text": "5.485", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Bandera_de_Espa%C3%B1a.svg/1200px-Bandera_de_Espa%C3%B1a.svg.png"},
        ]
        for card_element in cards_col1:
            card(
                title=card_element["title"],
                text=card_element["text"],
                image=card_element["image"],
                key=card_element["title"],
                on_click=lambda: print("Clicked!"),
                styles={
                    "card": {
                        "margin": "0",
                    }}
            )
