import pandas as pd
import streamlit as st

# Load your custom CSS file
with open("styles.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
st.title("Taller 1 - Big Data")
st.header("Universidad de los Andes")
st.header("Grupo 03")
st.subheader("Integrantes: Juan David Ayala, Brayan García, Alberto Mendoza")
st.subheader("{aj.mendoza, bs.garciac1, jd.ayalan1} @uniandes.edu.co")
st.header("Estructura de aplicación")
st.subheader("La aplicación está compuesta por dos secciones: Noticias y taxis, las cuales corresponden al punto 1 y 2 del taller respectivamente. Selecione una de las dos opciones del menú de la izquierda para ver las soluciones del Taller.")
